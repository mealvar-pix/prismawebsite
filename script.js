/* ==========================================================
   PRISMA INTELIGENTE · configuración central + interacción
   ----------------------------------------------------------
   Edite SOLO este objeto para cambiar datos de contacto,
   perfil del segundo fundador, formulario y enlaces.
   Los valores en null se muestran como PLACEHOLDER mientras
   showPlaceholders sea true; con false se ocultan.
   ========================================================== */
const PRISMA_CONFIG = {
  company: {
    name: 'PRISMA Inteligente',
    tagline: 'Más perspectiva. Mejores decisiones.',
    location: null            // PLACEHOLDER · ej.: 'San José, Costa Rica'
  },
  contact: {
    email: null,              // PLACEHOLDER · ej.: 'contacto@prismainteligente.com'
    phone: null,              // PLACEHOLDER · ej.: '+506 0000 0000'
    linkedin: null            // PLACEHOLDER · URL de la página de LinkedIn de la empresa
  },
  form: {
    // 'netlify'  → Netlify Forms (sin backend, recomendado si publica en Netlify)
    // 'endpoint' → POST JSON a `endpoint` (Formspree, Getform, API propia…)
    // 'demo'     → solo valida y muestra confirmación (no envía nada)
    provider: 'demo',
    endpoint: null            // ej.: 'https://formspree.io/f/XXXXXXX'
  },
  links: {
    intelligenceUrl: null,    // URL de PRISMA Intelligence cuando exista; si es null, el botón abre el formulario
    teamUrl: null,            // página de equipo; si es null, el botón baja a los perfiles
    insightsUrl: null         // listado de insights; si es null, se queda en la sección
  },
  // URL de cada artículo cuando se publique (clave = data-insight del HTML)
  insights: {
    'capacidad-liberada': null,
    'puente-variaciones': null,
    'forecast-13-semanas': null,
    'dashboard-no-es-sistema': null,
    'comprar-mas-barato': null
  },
  founders: [
    {
      name: 'Melissa Alvarado Ugalde',
      role: 'Cofundadora',
      photo: null,            // ej.: 'assets/img/founder-melissa.jpg'
      linkedin: null
    },
    {
      name: 'Francisco Barboza',
      role: 'Cofundador',     // PLACEHOLDER · confirmar cargo
      photo: null,            // ej.: 'assets/img/founder-francisco.jpg'
      linkedin: null,
      credentials: [],        // ej.: ['Ingeniero Industrial', 'MBA']
      bio: null               // PLACEHOLDER · 2–3 líneas de trayectoria
    }
  ],
  showPlaceholders: true
};

(function () {
  'use strict';
  const C = PRISMA_CONFIG;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (v) => String(v).replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
  const ph = (label) => (C.showPlaceholders ? `<span class="ph">PLACEHOLDER · ${esc(label)}</span>` : '');
  const icon = (id) => `<svg class="ic" aria-hidden="true"><use href="#i-${id}"/></svg>`;

  /* ---------- Año dinámico y nombre ---------- */
  $('#year').textContent = new Date().getFullYear();
  $$('[data-company-name]').forEach((el) => { el.textContent = C.company.name; });

  /* ---------- Datos de contacto ---------- */
  const list = $('#contact-list');
  const rows = [
    ['mail', 'Correo', C.contact.email, 'correo de contacto'],
    ['phone', 'Teléfono', C.contact.phone, 'teléfono'],
    ['pin', 'Ubicación', C.company.location, 'ciudad y país'],
    ['linkedin', 'LinkedIn', C.contact.linkedin, 'URL de LinkedIn']
  ];
  list.innerHTML = rows.map(([ic, label, val, phLabel]) => {
    if (!val) return C.showPlaceholders ? `<li>${icon(ic)}${ph(phLabel)}</li>` : '';
    if (ic === 'linkedin') return `<li>${icon(ic)}<a href="${esc(val)}" target="_blank" rel="noopener">LinkedIn de ${esc(C.company.name)}</a></li>`;
    const copy = ic === 'mail' || ic === 'phone' ? `<button type="button" class="copy-btn" data-copy="${esc(val)}">${icon('copy')}Copiar</button>` : '';
    return `<li>${icon(ic)}<span class="sr-label" hidden>${label}</span><span class="val">${esc(val)}</span>${copy}</li>`;
  }).join('');
  list.addEventListener('click', (e) => {
    const b = e.target.closest('[data-copy]');
    if (!b) return;
    const text = b.dataset.copy;
    const done = () => { b.lastChild.textContent = 'Copiado'; setTimeout(() => { b.lastChild.textContent = 'Copiar'; }, 1800); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(() => selectText(b.previousElementSibling));
    } else selectText(b.previousElementSibling);
  });
  function selectText(el) { const r = document.createRange(); r.selectNodeContents(el); const s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }

  const social = $('#footer-social');
  social.innerHTML = C.contact.linkedin
    ? `<a href="${esc(C.contact.linkedin)}" target="_blank" rel="noopener" aria-label="LinkedIn de ${esc(C.company.name)}">${icon('linkedin')} LinkedIn</a>`
    : ph('LinkedIn');

  /* ---------- Fundadores ---------- */
  C.founders.forEach((f, i) => {
    const role = $(`[data-founder-role="${i}"]`);
    if (role && f.role) role.textContent = f.role;
    const photo = $(`[data-founder-photo="${i}"]`);
    if (photo && f.photo) {
      const img = new Image();
      img.alt = `Fotografía de ${f.name}`;
      img.src = f.photo;
      img.onerror = () => img.remove();
      photo.appendChild(img);
    }
    const li = $(`[data-founder-linkedin="${i}"]`);
    if (li && f.linkedin) { li.href = f.linkedin; li.target = '_blank'; li.rel = 'noopener'; li.hidden = false; }
    const creds = $(`[data-founder-creds="${i}"]`);
    if (creds && f.credentials && f.credentials.length) creds.innerHTML = f.credentials.map((c) => `<li>${esc(c)}</li>`).join('');
    const bio = $(`[data-founder-bio="${i}"]`);
    if (bio) {
      if (f.bio) bio.textContent = f.bio;
      else if (!C.showPlaceholders) bio.hidden = true;
    }
  });

  /* ---------- Enlaces configurables ---------- */
  const intel = $('[data-intel-link]');
  if (intel && C.links.intelligenceUrl) { intel.href = C.links.intelligenceUrl; intel.removeAttribute('data-prefill'); }
  const team = $('[data-team-link]');
  if (team && C.links.teamUrl) team.href = C.links.teamUrl;
  const allIns = $('[data-insights-link]');
  if (allIns) {
    if (C.links.insightsUrl) allIns.href = C.links.insightsUrl;
    else { allIns.href = '#contacto'; allIns.dataset.prefill = 'Quiero recibir los PRISMA Insights cuando se publiquen'; allIns.firstChild.textContent = 'Recibir los insights cuando se publiquen '; }
  }
  $$('[data-insight]').forEach((card) => {
    const url = C.insights[card.dataset.insight];
    if (!url) return;
    const a = document.createElement('a');
    a.className = 'insight-link'; a.href = url; a.setAttribute('aria-label', card.querySelector('h3').textContent);
    card.appendChild(a);
    const st = card.querySelector('[data-insight-status]');
    if (st) st.textContent = 'Leer artículo';
  });

  /* ---------- Header y menú móvil ---------- */
  const header = $('.site-header');
  const toggle = $('.menu-toggle');
  const nav = $('#main-nav');
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    nav.classList.toggle('open', open);
    document.body.classList.toggle('nav-open', open);
    if (open) { const first = nav.querySelector('a'); if (first) first.focus(); }
  }
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); toggle.focus(); } });
  window.matchMedia('(min-width: 1025px)').addEventListener('change', (m) => { if (m.matches) setMenu(false); });

  /* ---------- Navegación activa (scrollspy) ---------- */
  const navLinks = $$('.main-nav ul a');
  const groups = {
    inicio: ['inicio'],
    'que-hacemos': ['que-hacemos', 'metodologia', 'servicios', 'programas', 'valor'],
    capacidades: ['capacidades', 'activos'],
    intelligence: ['intelligence'], nosotros: ['nosotros'], insights: ['insights'], contacto: ['contacto']
  };
  const owner = {};
  Object.entries(groups).forEach(([k, ids]) => ids.forEach((id) => { owner[id] = k; }));
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const key = owner[en.target.id];
      navLinks.forEach((a) => a.classList.toggle('active', a.getAttribute('href') === `#${key}`));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  Object.keys(owner).forEach((id) => { const el = document.getElementById(id); if (el) spy.observe(el); });

  /* ---------- Prellenado del formulario desde CTAs ---------- */
  const situ = $('#f-situacion');
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-prefill]');
    if (!a || a.getAttribute('href') !== '#contacto') return;
    const v = a.dataset.prefill;
    if (v && v !== 'Conversación inicial' && !situ.value.trim()) situ.value = `${v}. `;
    setTimeout(() => $('#f-nombre').focus({ preventScroll: true }), 650);
  });

  /* ---------- Animaciones de entrada (solo bajo el primer pliegue) ---------- */
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    const els = $$('.reveal');
    const vh = window.innerHeight;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.remove('pre'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach((el) => {
      if (el.getBoundingClientRect().top > vh) { el.classList.add('pre'); io.observe(el); }
    });
  }

  /* ---------- Formulario ---------- */
  const form = $('#contact-form');
  const status = $('#form-status');
  const btn = $('#f-submit');
  const rules = {
    nombre: (v) => (v.length < 2 ? 'Indique su nombre.' : ''),
    empresa: (v) => (v.length < 2 ? 'Indique el nombre de su empresa.' : ''),
    cargo: (v) => (v.length < 2 ? 'Indique su cargo.' : ''),
    pais: (v) => (v.length < 2 ? 'Indique el país.' : ''),
    email: (v) => (!v ? 'Indique su correo electrónico.' : (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : 'Revise el correo: debe tener el formato nombre@empresa.com.')),
    situacion: (v) => (v.length < 20 ? 'Describa la situación en al menos 20 caracteres para poder preparar la conversación.' : '')
  };
  function check(input) {
    const msg = rules[input.name] ? rules[input.name](input.value.trim()) : '';
    const field = input.closest('.field');
    const err = $(`#e-${input.name}`);
    field.classList.toggle('invalid', !!msg);
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (err) { err.textContent = msg; input.setAttribute('aria-describedby', err.id); }
    return !msg;
  }
  Object.keys(rules).forEach((name) => {
    const input = form.elements[name];
    input.addEventListener('blur', () => { if (input.value) check(input); });
    input.addEventListener('input', () => { if (input.closest('.field').classList.contains('invalid')) check(input); });
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    status.className = 'form-status'; status.textContent = '';
    const invalid = Object.keys(rules).map((n) => form.elements[n]).filter((i) => !check(i));
    if (invalid.length) {
      invalid[0].focus();
      status.className = 'form-status bad';
      status.textContent = invalid.length === 1 ? 'Revise el campo marcado.' : `Revise los ${invalid.length} campos marcados.`;
      return;
    }
    if (form.elements['empresa-web'].value) return; // honeypot anti-spam
    const data = new FormData(form);
    btn.disabled = true; btn.firstChild.textContent = 'Enviando… ';
    try {
      if (C.form.provider === 'netlify') {
        const res = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(data).toString() });
        if (!res.ok) throw new Error(res.status);
      } else if (C.form.provider === 'endpoint' && C.form.endpoint) {
        const res = await fetch(C.form.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(Object.fromEntries(data)) });
        if (!res.ok) throw new Error(res.status);
      } else {
        await new Promise((r) => setTimeout(r, 500));
      }
      form.reset();
      $$('.field', form).forEach((f) => f.classList.remove('invalid'));
      status.className = 'form-status ok';
      status.textContent = C.form.provider === 'demo'
        ? 'Formulario validado. Modo demostración: configure PRISMA_CONFIG.form para recibir las solicitudes.'
        : 'Gracias. Recibimos su solicitud y le escribiremos para coordinar una primera conversación.';
    } catch (err) {
      status.className = 'form-status bad';
      status.textContent = 'No se pudo enviar la solicitud. Revise su conexión e intente de nuevo.';
    } finally {
      btn.disabled = false; btn.firstChild.textContent = 'Enviar solicitud ';
    }
  });
})();
