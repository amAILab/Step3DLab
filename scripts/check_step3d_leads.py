#!/usr/bin/env python3
"""Check Gmail for new Step3D form submissions, auto-reply by email, and print alert.

Uses mcporter + google-workspace MCP OAuth. Keeps a local seen-id file so
OpenClaw can run it periodically without duplicate notifications.
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".lead_monitor_seen.json"
QUERY = 'newer_than:30d subject:"Новая заявка Step3D"'
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


LABELS = {
    "name": "Имя",
    "email": "Email",
    "contact": "Телефон / Telegram",
    "projectType": "Тип проекта",
    "deadline": "Срок",
    "quantity": "Количество",
    "dimensions": "Габариты",
    "hasFiles": "Файлы/фото",
    "description": "Описание",
    "source": "Источник",
    "page": "Страница",
    "submittedAt": "Время отправки",
}


def call_tool(tool: str, **kwargs: Any):
    cmd = [
        "mcporter",
        "call",
        "--server",
        "google-workspace",
        "--tool",
        tool,
        "--output",
        "json",
    ]
    for key, value in kwargs.items():
        cmd.append(f"{key}={value}")
    raw = subprocess.check_output(cmd, text=True)
    return json.loads(raw)


def load_seen() -> set[str]:
    if not STATE.exists():
        return set()
    try:
        return set(json.loads(STATE.read_text(encoding="utf-8")))
    except Exception:
        return set()


def save_seen(ids: set[str]) -> None:
    STATE.write_text(json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding="utf-8")


def extract_lead(body: str, snippet: str = "") -> dict[str, str]:
    pairs = re.findall(
        r"<strong>([^<]+)</strong>.*?<pre[^>]*>(.*?)</pre>",
        body,
        flags=re.S | re.I,
    )
    lead: dict[str, str] = {}
    for key, value in pairs:
        key = html_lib.unescape(key).strip()
        value = html_lib.unescape(re.sub(r"<[^>]+>", "", value)).strip()
        if key.startswith("_") or key == "_honey" or not value:
            continue
        lead[key] = value
    if not lead and snippet:
        lead["description"] = snippet.strip()
    return lead


def estimate_lead(lead: dict[str, str]) -> dict[str, str]:
    project = (lead.get("projectType") or "").lower()
    quantity = lead.get("quantity") or "не указано"
    dimensions = lead.get("dimensions") or "не указаны"
    has_files = (lead.get("hasFiles") or "").lower()

    if "реверс" in project or "скан" in project:
        return {
            "title": "3D-сканирование / реверс-инжиниринг",
            "timeline": "обычно 2–5 рабочих дней после получения детали, фото и критичных размеров",
            "price": "ориентир от 10 000 ₽ за задачу; точнее после понимания геометрии и требований к точности",
            "next": "нужны фото детали с разных сторон, общий размер и зоны, где важны посадки/точность",
        }
    if "мастер" in project or "обуч" in project:
        return {
            "title": "мастер-класс / образовательный проект",
            "timeline": "обычно 3–10 рабочих дней на согласование программы и подготовку материалов",
            "price": "стоимость зависит от длительности, количества участников, площадки и материалов",
            "next": "нужны возраст участников, количество человек, длительность и желаемый итог занятия",
        }
    if "собы" in project or "сцен" in project:
        return {
            "title": "объект для события / сцены",
            "timeline": "обычно от 5 рабочих дней, срочность зависит от размера и постобработки",
            "price": "ориентир от 20 000 ₽ за объект; точнее после референсов, размеров и даты мероприятия",
            "next": "нужны дата события, референсы по стилю, примерный размер и требования к внешнему виду",
        }
    if "сер" in project:
        return {
            "title": "прототип / малая серия",
            "timeline": "обычно 2–4 рабочих дня на прототип и затем расчёт партии",
            "price": "стоимость серии считаем после тестового образца; зависит от материала, времени печати и количества",
            "next": f"для партии {quantity} шт. нужны файл/фото, размеры ({dimensions}) и требования к материалу",
        }
    # Default: 3D print / modelling
    model_note = "Если готовой 3D-модели нет, подготовка модели считается отдельно."
    if "stl" in has_files or "step" in has_files or "obj" in has_files or "3mf" in has_files:
        model_note = "Если файл уже готов к печати, отдельно считаем только печать и возможную подготовку файла."
    return {
        "title": "3D-печать детали",
        "timeline": "обычно 1–3 рабочих дня после согласования модели, материала и параметров печати",
        "price": "предварительный ориентир для простой детали около 100 мм: 1 500–2 500 ₽ за штуку; моделирование при необходимости — отдельно, обычно от 3 000–7 000 ₽",
        "next": f"для точного расчёта нужны фото/эскиз или STL/STEP-файл, размеры ({dimensions}), назначение детали и требования к прочности/поверхности. {model_note}",
    }


def build_reply(lead: dict[str, str]) -> tuple[str, str]:
    name = lead.get("name") or ""
    greeting = f"Здравствуйте, {name}!" if name else "Здравствуйте!"
    project = lead.get("projectType") or "задача Step3D"
    quantity = lead.get("quantity") or "не указано"
    dimensions = lead.get("dimensions") or "не указаны"
    deadline = lead.get("deadline") or "не указан"
    estimate = estimate_lead(lead)

    subject = f"Step3D — предварительная оценка заявки: {project}"
    body = f"""{greeting}

Спасибо за заявку в Step3D.

Мы посмотрели вводные:
— тип проекта: {project};
— количество: {quantity};
— габариты: {dimensions};
— желаемый срок: {deadline}.

Предварительная оценка
Направление: {estimate['title']}.
Срок: {estimate['timeline']}.
Стоимость: {estimate['price']}.

Что нужно для точного расчёта
{estimate['next']}

Пожалуйста, пришлите ответным письмом фото, эскиз, чертёж или 3D-файл, если он есть. Если удобнее отправить файлы в Telegram, можно написать менеджеру: https://t.me/step_3d_mngr

После получения материалов мы уточним технологию, риски, срок и финальную стоимость.

С уважением,
Step3D
3D-печать · моделирование · прототипирование
https://amailab.github.io/Step3D/
"""
    return subject, body


def send_auto_reply(lead: dict[str, str], *, dry_run: bool = False) -> str:
    email = (lead.get("email") or "").strip()
    if not email:
        return "автоответ не отправлен: email не указан"
    if not EMAIL_RE.match(email):
        return f"автоответ не отправлен: некорректный email `{email}`"
    subject, body = build_reply(lead)
    if dry_run:
        return f"dry-run: автоответ НЕ отправлен на {email}; тема черновика: {subject}"
    call_tool("gmail.send", to=email, subject=subject, body=body)
    return f"автоответ отправлен на {email}"


def format_summary(lead: dict[str, str]) -> str:
    useful = []
    for key in [
        "name",
        "email",
        "contact",
        "projectType",
        "deadline",
        "quantity",
        "dimensions",
        "hasFiles",
        "description",
        "source",
        "page",
        "submittedAt",
    ]:
        value = lead.get(key)
        if value:
            useful.append(f"{LABELS.get(key, key)}: {value}")
    if not useful:
        return "Новая заявка без распознанного текста"
    return "\n".join(useful[:12])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Step3D Gmail leads and print alerts.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="do not send auto-replies and do not mark new leads as seen",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    seen = load_seen()
    try:
        result = call_tool("gmail.search", query=QUERY, maxResults=10)
    except subprocess.CalledProcessError as exc:
        print(f"LEAD_MONITOR_UNAVAILABLE: google-workspace/mcporter недоступен (exit {exc.returncode}).")
        return 2
    messages = result.get("messages", []) or []
    ids = [m["id"] for m in messages if m.get("id")]

    if not STATE.exists():
        save_seen(set(ids))
        print("NO_NEW_LEADS: мониторинг заявок Step3D инициализирован.")
        return 0

    new_ids = [mid for mid in ids if mid not in seen]
    if not new_ids:
        print("NO_NEW_LEADS")
        return 0

    alerts = []
    for mid in reversed(new_ids):
        msg = call_tool("gmail.get", messageId=mid)
        body = (msg.get("body") or msg.get("snippet") or "").strip()
        lead = extract_lead(body, msg.get("snippet") or "")
        reply_status = send_auto_reply(lead, dry_run=args.dry_run)
        if not args.dry_run:
            seen.add(mid)
        alerts.append(
            "🦞 Новая заявка Step3D\n"
            f"Тема: {msg.get('subject', 'без темы')}\n"
            f"От: {msg.get('from', 'неизвестно')}\n"
            f"Дата: {msg.get('date', '')}\n\n"
            f"{format_summary(lead)}\n\n"
            f"✉️ {reply_status}"
        )

    if not args.dry_run:
        save_seen(seen)
    print("\n\n---\n\n".join(alerts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
