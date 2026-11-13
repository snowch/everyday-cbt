/* All learning content is pre-rendered. Only progress IDs are stored locally. */
(() => {
  'use strict';
  const KEY = 'everyday-cbt-progress-v1';
  let state = { viewed: [], tried: [], last: null };
  let storageAvailable = true;
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved && Array.isArray(saved.viewed) && Array.isArray(saved.tried)) {
      state = { viewed: saved.viewed.filter(x => /^c\d{2}p\d{2}$/.test(x)), tried: saved.tried.filter(x => /^c\d{2}p\d{2}$/.test(x)), last: saved.last };
    }
  } catch { storageAvailable = false; }
  const unique = values => [...new Set(values)];
  function save() {
    state.viewed = unique(state.viewed); state.tried = unique(state.tried);
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch { storageAvailable = false; }
    updateProgress();
  }
  function updateProgress() {
    document.querySelectorAll('[data-progress]').forEach(el => {
      const card = el.closest('.chapter');
      const number = [...card.parentElement.children].indexOf(card) + 1;
      const prefix = `c${String(number).padStart(2, '0')}p`;
      const viewed = state.viewed.filter(x => x.startsWith(prefix)).length;
      const tried = state.tried.filter(x => x.startsWith(prefix)).length;
      el.textContent = viewed ? `${viewed}/8 pages viewed · ${tried}/4 practices tried` : 'Not yet viewed';
    });
    const caption = document.querySelector('[data-chapter-progress]');
    if (caption) {
      const ids = [...document.querySelectorAll('.lesson-page')].map(el => el.dataset.id);
      const viewed = ids.filter(x => state.viewed.includes(x)).length;
      const tried = ids.filter(x => state.tried.includes(x)).length;
      caption.textContent = `${viewed}/8 pages viewed · ${tried}/4 practices tried.${storageAvailable ? '' : ' Progress won’t be saved in this browser.'}`;
    }
  }
  const resume = document.getElementById('resume-learning');
  if (resume && state.last && Number.isInteger(state.last.page) && state.last.page >= 1 && state.last.page <= 8) {
    const link = [...document.querySelectorAll('.chapter-link')].find(el => el.dataset.slug === state.last.slug);
    if (link) { resume.href = link.getAttribute('href') + '#p' + state.last.page; resume.hidden = false; }
  }
  updateProgress();
  const player = document.querySelector('[data-chapter]');
  if (player) {
    const pages = [...player.querySelectorAll('.lesson-page')];
    const previous = document.getElementById('previous-page');
    const next = document.getElementById('next-page');
    const chapterOptions = player.querySelector('.chapter-options');
    if (chapterOptions) {
      document.addEventListener('click', event => {
        if (chapterOptions.open && !chapterOptions.contains(event.target)) chapterOptions.open = false;
      });
      chapterOptions.addEventListener('keydown', event => {
        if (event.key === 'Escape') { chapterOptions.open = false; chapterOptions.querySelector('summary').focus(); }
      });
    }
    let current = 0;
    function show(focus = false) {
      const match = location.hash.match(/^#p([1-8])$/);
      current = match ? Number(match[1]) - 1 : 0;
      pages.forEach((page, index) => {
        page.hidden = index !== current;
        page.querySelectorAll('audio').forEach(audio => { if (index !== current) { audio.pause(); try { audio.currentTime = 0; } catch {} } });
      });
      previous.disabled = current === 0; next.disabled = current === pages.length - 1;
      const options = player.querySelector('.chapter-options'); if (options) options.open = false;
      document.getElementById('page-status').textContent = `Page ${current + 1} of ${pages.length} · ${pages[current].querySelector('.lesson-stage').textContent}`;
      document.querySelectorAll('[data-page-link]').forEach(link => {
        if (Number(link.dataset.pageLink) === current) link.setAttribute('aria-current', 'step');
        else link.removeAttribute('aria-current');
      });
      state.viewed.push(pages[current].dataset.id);
      state.last = { slug: player.dataset.chapter, page: current + 1 }; save();
      if (focus) { pages[current].focus({ preventScroll: true }); pages[current].scrollIntoView({ block: 'start' }); }
    }
    function move(delta) {
      const index = current + delta;
      if (index >= 0 && index < pages.length) location.hash = 'p' + (index + 1);
    }
    previous.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    player.querySelectorAll('[data-step]').forEach(button => button.addEventListener('click', () => move(Number(button.dataset.step))));
    addEventListener('hashchange', () => show(true));
    document.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.target.closest('input,textarea,select,button,summary,a,[contenteditable]')) return;
      if (event.key === 'ArrowRight') { event.preventDefault(); move(1); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1); }
    });
    show();
  }
  document.querySelectorAll('.decision-form').forEach(form => {
    form.addEventListener('change', () => form.querySelectorAll('[data-feedback]').forEach(el => { el.hidden = true; }));
    form.addEventListener('submit', event => {
      event.preventDefault();
      const choice = form.querySelector('input:checked');
      if (!choice) { form.reportValidity(); return; }
      form.querySelectorAll('[data-feedback]').forEach(el => { el.hidden = el.dataset.feedback !== choice.value; });
      state.tried.push(form.dataset.practice); save();
    });
  });
  document.querySelectorAll('[data-tried]').forEach(button => {
    if (state.tried.includes(button.dataset.tried)) button.textContent = 'Practice marked as tried';
    button.addEventListener('click', () => { state.tried.push(button.dataset.tried); save(); button.textContent = 'Practice marked as tried'; });
  });
  document.querySelectorAll('.audio-rate').forEach(select => select.addEventListener('change', () => {
    document.querySelectorAll('.audio-rate').forEach(other => { other.value = select.value; });
    document.querySelectorAll('audio').forEach(audio => { audio.playbackRate = Number(select.value); });
  }));
  document.querySelectorAll('audio').forEach(audio => audio.addEventListener('play', () => {
    document.querySelectorAll('audio').forEach(other => { if (other !== audio) other.pause(); });
  }));
  document.querySelectorAll('[data-export]').forEach(button => button.addEventListener('click', () => {
    const parts = [document.title, 'Responses exported from this tab. No answers were submitted to a server.', ''];
    document.querySelectorAll('.decision-form').forEach(form => { const choice = form.querySelector('input:checked'); if (choice) { parts.push(form.closest('.lesson-page').querySelector('h2').textContent, choice.closest('label').textContent.trim(), ''); } });
    document.querySelectorAll('textarea').forEach(input => { if (input.value.trim()) parts.push(input.dataset.prompt, input.value, ''); });
    const blob = new Blob([parts.join('\n\n')], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob); const link = document.createElement('a');
    link.href = url; link.download = 'everyday-cbt-responses.txt'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }));
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  document.querySelectorAll('[data-clear-progress]').forEach(button => button.addEventListener('click', () => {
    state = { viewed: [], tried: [], last: null };
    try { localStorage.removeItem(KEY); } catch {}
    updateProgress(); const message = document.querySelector('[data-storage-message]');
    if (message) message.textContent = 'Saved course progress cleared on this device.';
  }));
  // Print current responses as text, including text that extends beyond a textarea.
  addEventListener('beforeprint', () => {
    document.querySelectorAll('.printed-response').forEach(el => el.remove());
    document.querySelectorAll('textarea').forEach(input => {
      const text = document.createElement('div'); text.className = 'printed-response';
      text.textContent = input.value || '\n\n\n'; input.after(text);
    });
  });
  addEventListener('afterprint', () => document.querySelectorAll('.printed-response').forEach(el => el.remove()));
})();
