/* All learning content is pre-rendered. Only progress IDs are stored locally. */
(() => {
  'use strict';
  const KEY = 'everyday-cbt-progress-v1';
  const empty = () => ({ viewed: [], tried: [], last: null });
  const lessonId = /^c(?:0[1-9]|1[0-2])p0[1-8]$/;
  const practiceId = /p0[2678]$/;
  const unique = values => [...new Set(values)];
  let saved = empty();
  let pending = empty();
  let storageMessage = '';

  function readProgress() {
    try {
      const value = localStorage.getItem(KEY);
      if (value === null) return empty();
      const record = JSON.parse(value);
      if (!Array.isArray(record?.viewed) || !Array.isArray(record?.tried)) throw new Error('Invalid progress');
      const valid = value => typeof value === 'string' && lessonId.test(value);
      return {
        viewed: unique(record.viewed.filter(valid)),
        tried: unique(record.tried.filter(value => valid(value) && practiceId.test(value))),
        last: record.last,
      };
    } catch {
      storageMessage = 'Saved progress can’t be read. New progress won’t be saved until it can be read again.';
      return null;
    }
  }

  function combinedProgress() {
    return {
      viewed: unique([...saved.viewed, ...pending.viewed]),
      tried: unique([...saved.tried, ...pending.tried]),
      last: pending.last ?? saved.last,
    };
  }

  function saveProgress() {
    const latest = readProgress();
    if (latest) {
      saved = latest;
      try {
        const next = combinedProgress();
        localStorage.setItem(KEY, JSON.stringify(next));
        saved = next;
        pending = empty();
        storageMessage = '';
      } catch {
        storageMessage = 'New progress won’t be saved until this browser allows writing again.';
      }
    }
    updateProgress();
  }

  function progressText(viewed, tried) {
    return `${viewed} of 8 pages viewed · ${tried} of 4 practices tried`;
  }

  function updateProgress() {
    const state = combinedProgress();
    document.querySelectorAll('[data-progress]').forEach((el, index) => {
      const prefix = `c${String(index + 1).padStart(2, '0')}p`;
      const viewed = state.viewed.filter(id => id.startsWith(prefix)).length;
      const tried = state.tried.filter(id => id.startsWith(prefix)).length;
      el.textContent = viewed || tried ? progressText(viewed, tried) : 'Not yet viewed';
    });
    const caption = document.querySelector('[data-chapter-progress]');
    if (caption) {
      const ids = [...document.querySelectorAll('.lesson-page')].map(el => el.dataset.id);
      const viewed = ids.filter(id => state.viewed.includes(id)).length;
      const tried = ids.filter(id => state.tried.includes(id)).length;
      caption.textContent = progressText(viewed, tried);
    }
    document.querySelectorAll('[data-progress-status]').forEach(el => {
      el.textContent = storageMessage;
      el.hidden = !storageMessage;
    });
    document.querySelectorAll('[data-tried]').forEach(button => {
      const tried = state.tried.includes(button.dataset.tried);
      const savedHere = saved.tried.includes(button.dataset.tried);
      button.setAttribute('aria-disabled', String(savedHere));
      const caption = button.nextElementSibling;
      const status = savedHere ? 'Practice marked as tried.' : tried ? 'Practice marked as tried for this visit.' : '';
      if (caption.textContent !== status) caption.textContent = status;
    });
    const resume = document.getElementById('resume-learning');
    if (resume) {
      const last = state.last;
      const link = Number.isInteger(last?.page) && last.page >= 1 && last.page <= 8
        ? [...document.querySelectorAll('.chapter-link')].find(el => el.dataset.slug === last.slug)
        : null;
      if (link) resume.href = link.getAttribute('href') + '#p' + last.page;
      resume.hidden = !link;
      document.getElementById('start-learning').hidden = Boolean(link);
    }
  }

  saved = readProgress() ?? empty();
  updateProgress();
  addEventListener('storage', event => {
    if (event.storageArea !== localStorage || (event.key !== KEY && event.key !== null)) return;
    if (event.newValue === null) pending = empty();
    const latest = readProgress();
    if (latest) {
      saved = latest;
      if (!pending.viewed.length && !pending.tried.length) storageMessage = '';
    }
    updateProgress();
  });
  const player = document.querySelector('[data-chapter]');
  if (player) {
    const pages = [...player.querySelectorAll('.lesson-page')];
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
    function focusPage() {
      pages[current].focus({ preventScroll: true });
      pages[current].scrollIntoView({ block: 'start' });
    }
    document.querySelector('.skip').addEventListener('click', event => {
      event.preventDefault();
      focusPage();
    });
    function show(focus = false) {
      const match = location.hash.match(/^#p([1-8])$/);
      current = match ? Number(match[1]) - 1 : 0;
      pages.forEach((page, index) => {
        page.hidden = index !== current;
        page.querySelectorAll('audio').forEach(audio => { if (index !== current) { audio.pause(); try { audio.currentTime = 0; } catch {} } });
      });
      if (chapterOptions) chapterOptions.open = false;
      document.getElementById('page-status').textContent = `Page ${current + 1} of ${pages.length}`;
      document.querySelectorAll('[data-page-link]').forEach(link => {
        if (Number(link.dataset.pageLink) === current) link.setAttribute('aria-current', 'step');
        else link.removeAttribute('aria-current');
      });
      pending.viewed.push(pages[current].dataset.id);
      pending.last = { slug: player.dataset.chapter, page: current + 1 };
      saveProgress();
      if (focus) focusPage();
    }
    function move(delta) {
      const index = current + delta;
      if (index >= 0 && index < pages.length) location.hash = 'p' + (index + 1);
    }
    player.querySelectorAll('[data-step]').forEach(button => button.addEventListener('click', () => move(Number(button.dataset.step))));
    addEventListener('hashchange', () => show(true));
    document.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.target.closest('input,textarea,select,button,summary,a,audio,[contenteditable]')) return;
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
      const feedback = form.querySelectorAll('[data-feedback]');
      feedback.forEach(el => { el.hidden = el.dataset.feedback !== choice.value; });
      feedback[Number(choice.value)].focus();
      pending.tried.push(form.dataset.practice);
      saveProgress();
    });
  });
  document.querySelectorAll('[data-tried]').forEach(button => {
    button.addEventListener('click', () => {
      const id = button.dataset.tried;
      if (combinedProgress().tried.includes(id) && !pending.tried.includes(id)) return;
      pending.tried.push(id);
      saveProgress();
    });
  });
  document.querySelectorAll('.audio-rate').forEach(select => select.addEventListener('change', () => {
    document.querySelectorAll('.audio-rate').forEach(other => { other.value = select.value; });
    document.querySelectorAll('audio').forEach(audio => { audio.playbackRate = Number(select.value); });
  }));
  document.querySelectorAll('audio').forEach(audio => audio.addEventListener('play', () => {
    document.querySelectorAll('audio').forEach(other => { if (other !== audio) other.pause(); });
  }));
  document.querySelectorAll('[data-export]').forEach(button => button.addEventListener('click', () => {
    const parts = [document.title, 'Responses from this chapter or practice page. The course did not submit them anywhere.', ''];
    document.querySelectorAll('.decision-form').forEach(form => { const choice = form.querySelector('input:checked'); if (choice) { parts.push(form.closest('.lesson-page').querySelector('h2').textContent, choice.closest('label').textContent.trim(), ''); } });
    document.querySelectorAll('textarea').forEach(input => { if (input.value.trim()) parts.push(input.closest('section').querySelector('h2, h3')?.textContent || '', input.dataset.prompt, input.value, ''); });
    const blob = new Blob([parts.join('\n\n')], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob); const link = document.createElement('a');
    link.href = url; link.download = 'everyday-cbt-responses.txt'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }));
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  document.querySelectorAll('[data-clear-progress]').forEach(button => button.addEventListener('click', () => {
    const message = document.querySelector('[data-storage-message]');
    if (!confirm('Clear this course’s saved progress in this browser?')) {
      message.textContent = 'Saved progress was kept.';
      return;
    }
    try {
      localStorage.removeItem(KEY);
    } catch {
      message.textContent = 'Could not clear saved progress. It may still be saved in this browser.';
      return;
    }
    saved = empty();
    pending = empty();
    storageMessage = '';
    updateProgress();
    message.textContent = 'Saved course progress cleared in this browser.';
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
