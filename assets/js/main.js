'use strict';
(() => {
  const doc = document;
  const toggle = doc.querySelector('[data-menu-toggle]');
  const closeMenu = () => {
    doc.body.classList.remove('menu-open');
    if (toggle) { toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Открыть меню'); }
  };
  if (toggle) {
    toggle.addEventListener('click', () => {
      const open = doc.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    });
    doc.querySelectorAll('.main-nav a').forEach(link => link.addEventListener('click', closeMenu));
    doc.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
    window.addEventListener('resize', () => { if (window.innerWidth > 900) closeMenu(); });
  }

  // Reveal only after feature detection. The page remains readable without JS.
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const items = [...doc.querySelectorAll('.reveal')];
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }, { threshold: 0.07, rootMargin: '0px 0px -28px 0px' });
    items.forEach(el => { const rect = el.getBoundingClientRect(); if (rect.top < window.innerHeight + 80) el.classList.add('is-visible'); });
    doc.body.classList.add('motion-on');
    items.forEach(el => observer.observe(el));
  }

  const calc = doc.querySelector('[data-calculator]');
  if (calc) {
    const fields = {
      vehicle: calc.querySelector('[name="vehicle"]'),
      hours: calc.querySelector('[name="hours"]'),
      km: calc.querySelector('[name="km"]'),
      night: calc.querySelector('[name="night"]')
    };
    const output = calc.querySelector('[data-estimate]');
    const toast = calc.querySelector('[data-toast]');
    const buildMessage = () => {
      const hours = Math.max(1, Math.min(24, Number(fields.hours.value) || 1));
      const km = Math.max(0, Math.min(500, Number(fields.km.value) || 0));
      return `Здравствуйте! Нужен рефрижератор MiniRef.\nМашина: ${fields.vehicle.value}\nВремя в работе: ${hours} ч\nКм за МКАД: ${km}\nНочной рейс: ${fields.night.checked ? 'да' : 'нет'}\nПрошу уточнить доступность и стоимость.`;
    };
    const update = () => {
      const hours = Math.max(1, Math.min(24, Number(fields.hours.value) || 1));
      const km = Math.max(0, Math.min(500, Number(fields.km.value) || 0));
      output.textContent = `${fields.vehicle.value} · ${hours} ч · ${km} км за МКАД${fields.night.checked ? ' · ночной рейс' : ''}`;
      toast.textContent = '';
    };
    calc.addEventListener('input', update);
    calc.addEventListener('change', update);
    calc.addEventListener('submit', async event => {
      event.preventDefault();
      const message = buildMessage();
      try {
        if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(message);
        else {
          const temp = doc.createElement('textarea');
          temp.value = message; temp.style.position = 'fixed'; temp.style.opacity = '0';
          doc.body.appendChild(temp); temp.select();
          if (!doc.execCommand('copy')) throw new Error('copy failed');
          temp.remove();
        }
        toast.textContent = 'Параметры скопированы. Сообщите их менеджеру при обращении.';
      } catch (_) {
        window.prompt('Скопируйте параметры заявки:', message);
        toast.textContent = 'Параметры подготовлены.';
      }
    });
    update();
  }
})();
