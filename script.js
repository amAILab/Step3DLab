const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');
navToggle?.addEventListener('click', () => {
  const isOpen = nav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
});
nav?.addEventListener('click', (event) => {
  if (event.target.matches('a')) {
    nav.classList.remove('open');
    navToggle?.setAttribute('aria-expanded', 'false');
  }
});

document.querySelector('#briefForm')?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget).entries());
  const message = `Заявка Step3D Lab\n\nЗадача: ${data.task || '—'}\nЧто есть: ${data.source || '—'}\nКоличество/срок: ${data.deadline || '—'}\nКонтакт: ${data.contact || '—'}`;
  const output = document.querySelector('#briefOutput');
  output.textContent = message;
  try {
    await navigator.clipboard.writeText(message);
    output.textContent = `${message}\n\nТекст скопирован — можно отправить в Telegram.`;
  } catch {
    output.textContent = `${message}\n\nСкопируйте текст и отправьте в Telegram.`;
  }
  const tg = document.querySelector('#tgLink');
  tg.href = `https://t.me/step_3d_mngr?text=${encodeURIComponent(message)}`;
});
