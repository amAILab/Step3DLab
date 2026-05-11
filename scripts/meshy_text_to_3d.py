#!/usr/bin/env python3
"""Minimal Meshy Text-to-3D client for STEP 3D.

Usage:
  MESHY_API_KEY=msy_... python3 scripts/meshy_text_to_3d.py "industrial robot gripper" --formats glb stl

The API key is read only from the environment. Do not commit keys.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://api.meshy.ai/openapi/v2"
OUT_DIR = Path("assets/generated/meshy")


def request_json(method: str, path: str, api_key: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Meshy API error {exc.code}: {body}") from exc


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        path.write_bytes(resp.read())


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Meshy Text-to-3D preview task and download model files.")
    parser.add_argument("prompt", help="Text prompt, max 600 chars")
    parser.add_argument("--formats", nargs="+", default=["glb"], choices=["glb", "obj", "fbx", "stl", "usdz", "3mf"], help="Output formats")
    parser.add_argument("--model", default="meshy-6", help="Meshy model id, e.g. meshy-6/latest")
    parser.add_argument("--timeout", type=int, default=900, help="Polling timeout in seconds")
    parser.add_argument("--poll", type=int, default=10, help="Polling interval in seconds")
    args = parser.parse_args()

    api_key = os.environ.get("MESHY_API_KEY")
    if not api_key:
        secret_env = Path.home() / ".openclaw" / "secrets" / "meshy.env"
        if secret_env.exists():
            for line in secret_env.read_text(encoding="utf-8").splitlines():
                if line.startswith("MESHY_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    if not api_key:
        raise SystemExit("Set MESHY_API_KEY in the environment or ~/.openclaw/secrets/meshy.env. Example: MESHY_API_KEY=msy_... python3 scripts/meshy_text_to_3d.py 'prompt'")
    if len(args.prompt) > 600:
        raise SystemExit("Prompt is longer than Meshy limit: 600 characters")

    payload = {
        "mode": "preview",
        "prompt": args.prompt,
        "ai_model": args.model,
        "target_formats": args.formats,
        "moderation": True,
    }
    created = request_json("POST", "/text-to-3d", api_key, payload)
    task_id = created.get("result") or created.get("id")
    if not task_id:
        print(json.dumps(created, ensure_ascii=False, indent=2))
        raise SystemExit("Could not find task id in Meshy response")

    print(f"Created Meshy task: {task_id}")
    deadline = time.time() + args.timeout
    task = {}
    while time.time() < deadline:
        task = request_json("GET", f"/text-to-3d/{task_id}", api_key)
        status = task.get("status", "unknown")
        progress = task.get("progress", "")
        print(f"status={status} progress={progress}")
        if status in {"SUCCEEDED", "FAILED", "CANCELED", "EXPIRED"}:
            break
        time.sleep(args.poll)

    if task.get("status") != "SUCCEEDED":
        print(json.dumps(task, ensure_ascii=False, indent=2))
        raise SystemExit("Meshy task did not succeed")

    model_urls = task.get("model_urls") or task.get("model_url") or {}
    if not isinstance(model_urls, dict):
        print(json.dumps(task, ensure_ascii=False, indent=2))
        raise SystemExit("No downloadable model_urls found")

    safe_id = str(task_id).replace("/", "_")
    saved = []
    for fmt, url in model_urls.items():
        if fmt not in args.formats or not url:
            continue
        dest = OUT_DIR / safe_id / f"model.{fmt}"
        download(url, dest)
        saved.append(dest)

    meta = OUT_DIR / safe_id / "task.json"
    meta.parent.mkdir(parents=True, exist_ok=True)
    meta.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Saved:")
    for path in saved + [meta]:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
