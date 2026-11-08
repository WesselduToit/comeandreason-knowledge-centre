/* Come and Reason Knowledge Centre — shared kit (v1)
   Data-driven renderers shared by every page. No dependencies. */
window.KC = (function () {
  'use strict';

  /* ---------- storage (safe when localStorage is unavailable) ---------- */
  const mem = {};
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return k in mem ? mem[k] : d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { mem[k] = v; } }
  };

  /* ---------- DOM helpers ---------- */
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  function el(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    if (attrs) for (const k in attrs) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];
      else if (k.startsWith('on')) n.addEventListener(k.slice(2), attrs[k]);
      else if (k === 'style') n.style.cssText = attrs[k];
      else if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    }
    for (const kid of kids.flat()) if (kid !== null && kid !== undefined && kid !== false) n.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
    return n;
  }
  const $ = (sel, root) => (root || document).querySelector(sel);
  const nodata = msg => el('p', { class: 'nodata' }, msg || 'No data for this section yet.');

  /* ---------- lens toggle (imposed law / design law), persisted site-wide ---------- */
  const LENS_KEY = 'cr-lens';
  function setLens(v) {
    document.body.dataset.lens = v;
    store.set(LENS_KEY, v);
    document.querySelectorAll('.lens-switch button').forEach(b => b.classList.toggle('on', b.dataset.lens === v));
    document.dispatchEvent(new CustomEvent('kc:lens', { detail: v }));
  }
  function lensBar(container, opts) {
    opts = opts || {};
    const bar = el('div', { class: 'lens-bar' },
      el('span', { class: 'lbl' }, opts.label || 'Read every text through'),
      el('span', { class: 'lens-switch' },
        el('button', { 'data-lens': 'imposed', class: 'imposed', onclick: () => setLens('imposed') }, opts.imposed || 'Imposed law'),
        el('button', { 'data-lens': 'design', class: 'design', onclick: () => setLens('design') }, opts.design || 'Design law')));
    container.append(bar);
    setLens(store.get(LENS_KEY, opts.initial || 'imposed'));
    return bar;
  }
  const lens = () => document.body.dataset.lens || 'imposed';

  /* ---------- quotes, sources, badges ---------- */
  function sourceChip(src) {
    if (!src) return null;
    if (typeof src === 'string') src = { file: src };
    const kids = [];
    if (src.label) kids.push(esc(src.label));
    if (src.url) kids.push(`<a href="${esc(src.url)}" target="_blank" rel="noopener">${esc(src.label ? 'web' : src.url.replace(/^https?:\/\//, ''))}</a>`);
    if (src.file) kids.push(`<code title="${esc(src.file)}">${esc(shortPath(src.file))}</code>`);
    if (src.locator) kids.push(`<span>${esc(src.locator)}</span>`);
    if (!kids.length) return null;
    return el('span', { class: 'src', html: '📎 ' + kids.join(' · ') });
  }
  function shortPath(p) { const parts = String(p).split(/[\\/]/); return parts.slice(-2).join('/'); }
  function quote(text, opts) {
    opts = opts || {};
    if (!text) return null;
    const voice = opts.voice || 'scripture';
    const q = el('blockquote', { class: 'q ' + voice });
    q.append(el('span', {}, text));
    const refBits = [];
    if (opts.ref) refBits.push(opts.ref);
    if (opts.version) refBits.push(opts.version);
    if (voice === 'remedy') refBits.push('The Remedy');
    if (opts.verify) refBits.push('wording from memory, verify');
    if (refBits.length) q.append(el('span', { class: 'ref' }, refBits.join(' · ')));
    const chip = sourceChip(opts.source);
    if (chip) q.append(chip);
    return q;
  }
  const voiceTag = v => el('span', { class: 'tag ' + v }, { scripture: 'Scripture', remedy: 'The Remedy', jennings: 'Jennings', egw: 'E. G. White', cole: 'Cole (study guide)' }[v] || v);
  const missingBadge = txt => el('span', { class: 'badge-missing' }, txt || 'Not in The Remedy (OT outside Genesis/Psalms)');
  const caveat = txt => txt ? el('div', { class: 'caveat' }, '⚠ ' + txt) : null;

  /* ---------- verse card: traditional + Remedy + two readings (lens-aware) ---------- */
  function verseCard(v) {
    const card = el('div', { class: 'vcard', 'data-id': v.id || '' });
    const head = el('div', { class: 'vhead' }, el('span', { class: 'vref' }, v.ref));
    const tags = el('span');
    if (v.group) tags.append(el('span', { class: 'tag scripture' }, v.group));
    if (v.hard) tags.append(el('span', { class: 'tag hard' }, 'hard case'));
    head.append(tags);
    card.append(head);
    const t = v.traditional;
    if (t && t.text) card.append(quote(t.text, { ref: v.ref, version: t.version, verify: t.verify, source: t.source }));
    if (v.remedy && v.remedy.text) card.append(quote(v.remedy.text, { voice: 'remedy', ref: v.remedy.ref || v.ref }));
    else card.append(el('div', { style: 'margin:6px 0' }, missingBadge(v.remedy_note)));
    if (v.imposed) card.append(el('div', { class: 'lens-panel imposed lens-imposed' }, el('span', { class: 'tag imposed' }, 'heard as'), v.imposed));
    if (v.design) {
      const d = el('div', { class: 'lens-panel design lens-design' }, el('span', { class: 'tag design' }, 'Jennings reads'), v.design);
      const chip = sourceChip(v.jennings_source); if (chip) d.append(el('div', {}, chip));
      card.append(d);
    }
    const c = caveat(v.caveat); if (c) card.append(c);
    return card;
  }
  function renderVerseExplorer(container, verses, opts) {
    opts = opts || {};
    container.innerHTML = '';
    if (!verses || !verses.length) { container.append(nodata()); return; }
    const groups = [...new Set(verses.map(v => v.group).filter(Boolean))];
    const state = { group: 'all', remedyOnly: false, hardOnly: false, q: '' };
    const filters = el('div', { class: 'filters' });
    const chip = (label, on, fn) => { const b = el('button', { class: 'chip' + (on ? ' on' : ''), onclick: () => { fn(); draw(); } }, label); return b; };
    const list = el('div');
    const count = el('p', { class: 'small' });
    function draw() {
      filters.innerHTML = '';
      filters.append(chip('All', state.group === 'all', () => state.group = 'all'));
      groups.forEach(g => filters.append(chip(g, state.group === g, () => state.group = g)));
      filters.append(chip('Remedy available', state.remedyOnly, () => state.remedyOnly = !state.remedyOnly));
      filters.append(chip('Hard cases', state.hardOnly, () => state.hardOnly = !state.hardOnly));
      filters.append(chip('🎲 Random verse', false, () => { const pick = verses[Math.floor(Math.random() * verses.length)]; state.q = pick.ref; state.group = 'all'; state.remedyOnly = false; state.hardOnly = false; }));
      filters.append(chip('Clear filters', false, () => { state.q = ''; state.group = 'all'; state.remedyOnly = false; state.hardOnly = false; }));
      list.innerHTML = '';
      const shown = verses.filter(v => (state.group === 'all' || v.group === state.group) && (!state.remedyOnly || (v.remedy && v.remedy.text)) && (!state.hardOnly || v.hard) && (!state.q || v.ref === state.q));
      shown.forEach(v => list.append(verseCard(v)));
      count.textContent = `${shown.length} of ${verses.length} passages` + (state.q ? ` · showing ${state.q}` : '');
    }
    container.append(filters, count, list);
    draw();
  }

  /* ---------- timeline with "ask before reveal" nodes ---------- */
  function renderTimeline(container, items, opts) {
    opts = opts || {};
    container.innerHTML = '';
    if (!items || !items.length) { container.append(nodata()); return; }
    const tl = el('div', { class: 'tl' });
    items.forEach((it, i) => {
      const node = el('div', { class: 'node' + (it.hard ? ' hard' : '') });
      const card = el('div', { class: 'card sub' });
      card.append(el('h3', { style: 'margin-top:0' }, (opts.numbered ? `${i + 1}. ` : '') + it.title), it.ref ? el('div', { class: 'small' }, it.ref) : null);
      if (it.text) card.append(quote(it.text, { voice: it.remedy ? 'remedy' : 'scripture', version: it.version, verify: it.verify, source: it.source }));
      if (opts.body) card.append(opts.body(it));
      if (opts.ask && opts.ask.length) {
        const ask = el('div', { class: 'ask' });
        opts.ask.forEach(a => ask.append(el('span', { class: 'tag scripture' }, a)));
        card.append(ask);
        const rev = el('div', { class: 'reveal' }, opts.reveal ? opts.reveal(it) : null);
        card.append(el('button', { class: 'btn sm ghost', onclick: e => { node.classList.toggle('open'); e.target.textContent = node.classList.contains('open') ? 'Hide' : (opts.revealLabel || 'Reveal'); } }, opts.revealLabel || 'Reveal'), rev);
      }
      node.append(card);
      tl.append(node);
    });
    container.append(tl);
    return tl;
  }

  /* ---------- sort bins (click to place, no drag needed) ---------- */
  function renderSortBins(container, cfg) {
    container.innerHTML = '';
    if (!cfg || !cfg.items || !cfg.items.length) { container.append(nodata()); return; }
    const pool = el('div', { class: 'pool' });
    const bins = el('div', { class: 'bins' });
    const binEls = {};
    cfg.bins.forEach(b => { const d = el('div', { class: 'bin', 'data-bin': b.id }, el('h4', {}, b.label)); binEls[b.id] = d; bins.append(d); });
    const result = el('div', { class: 'result-line' });
    let picked = null;
    const tokens = cfg.items.map(it => {
      const t = el('button', { class: 'token', title: 'Click, then click a bin' }, it.label);
      t.addEventListener('click', () => { picked = { it, t }; document.querySelectorAll('.token.pick').forEach(x => x.classList.remove('pick')); t.classList.add('pick'); t.style.borderColor = 'var(--accent2)'; result.textContent = `Now click the bin for "${it.label}".`; });
      pool.append(t); return t;
    });
    cfg.bins.forEach(b => binEls[b.id].addEventListener('click', () => {
      if (!picked) { result.textContent = 'Pick an item first.'; return; }
      const { it, t } = picked; picked = null; t.style.borderColor = '';
      binEls[b.id].append(t);
      const ok = it.answer === b.id;
      t.classList.remove('ok', 'no'); t.classList.add(ok ? 'ok' : 'no');
      t.title = it.note || '';
      result.innerHTML = '';
      result.append(el('b', { style: ok ? 'color:var(--good)' : 'color:var(--bad)' }, ok ? 'Yes. ' : 'Not where Jennings puts it. '), it.feedback || it.note || '');
      if (cfg.onPlace) cfg.onPlace(it, b, ok);
      const done = cfg.items.every(x => pool.contains(tokens[cfg.items.indexOf(x)]) === false);
      if (done && cfg.onDone) cfg.onDone();
    }));
    container.append(el('p', { class: 'small' }, cfg.hint || 'Click an item, then click the bin it belongs in.'), pool, bins, result);
  }

  /* ---------- flip pairs (said / happened) ---------- */
  function renderFlipPairs(container, pairs, labels) {
    labels = labels || { a: 'What God said', b: 'What actually happened' };
    container.innerHTML = '';
    if (!pairs || !pairs.length) { container.append(nodata()); return; }
    pairs.forEach(p => {
      const f = el('div', { class: 'flip' });
      const a = el('div', { class: 'side said' }, el('h4', {}, labels.a), p.said ? quote(p.said.text, { ref: p.said.ref, version: p.said.version, verify: p.said.verify }) : null,
        el('button', { class: 'btn sm ghost', onclick: () => f.classList.toggle('open') }, 'Then what happened?'));
      const b = el('div', { class: 'side happened' }, el('h4', {}, labels.b), p.happened ? quote(p.happened.text, { ref: p.happened.ref, version: p.happened.version, verify: p.happened.verify, voice: p.happened.remedy ? 'remedy' : 'scripture' }) : null,
        p.note ? el('div', { class: 'lens-panel design' }, el('span', { class: 'tag design' }, 'Jennings'), p.note, sourceChip(p.source)) : null);
      f.append(a, b);
      container.append(f);
    });
  }

  /* ---------- accordion (objections desk etc.) ---------- */
  function renderAccordion(container, items, opts) {
    opts = opts || {};
    container.innerHTML = '';
    if (!items || !items.length) { container.append(nodata()); return; }
    items.forEach((it, i) => {
      const d = el('details', { class: 'acc' });
      const s = el('summary', {}, (opts.numbered ? `${i + 1}. ` : '') + (it.title || it.objection || it.term));
      if (it.strength) s.append(' ', el('span', { class: 'tag ' + it.strength }, it.strength + ' evidence'));
      d.append(s);
      const body = el('div', { class: 'body' });
      if (opts.body) body.append(opts.body(it, i)); else body.append(it.body || it.meaning || '');
      d.append(body);
      container.append(d);
    });
  }

  /* ---------- level stepper (shared with the Seven Levels page) ---------- */
  function renderStepper(container, rows, onPick, initial) {
    container.innerHTML = '';
    if (!rows || !rows.length) { container.append(nodata()); return; }
    const st = el('div', { class: 'stepper' });
    let cur = initial || rows[0].n;
    const btns = rows.map(r => el('button', { onclick: () => { cur = r.n; paint(); onPick(r); } }, `${r.n} · ${r.name}`));
    btns.forEach(b => st.append(b));
    function paint() { btns.forEach((b, i) => { const on = rows[i].n === cur; b.classList.toggle('on', on); b.classList.toggle('l' + rows[i].n, on); }); }
    container.append(st, el('div', { class: 'divider-note' }, 'Levels 1–4 hear an imposed law; levels 5–7 hear a design law. The shift is between 4 and 5.'));
    paint(); onPick(rows.find(r => r.n === cur));
  }

  /* ---------- glossary popovers ---------- */
  let pop = null;
  function glossaryTerm(term, entry) {
    const s = el('span', { class: 'gl', tabindex: 0 }, term);
    const show = (ev) => {
      hidePop();
      pop = el('div', { class: 'pop' }, el('span', { class: 'x', onclick: hidePop }, '✕'), el('b', {}, entry.term || term), el('div', {}, entry.meaning || entry.gloss || ''));
      if (entry.greek) pop.append(el('div', { class: 'small' }, 'Greek: ' + entry.greek));
      if (entry.remedy && entry.remedy.text) pop.append(quote(entry.remedy.text, { voice: 'remedy', ref: entry.remedy.ref }));
      if (entry.caveat) pop.append(caveat(entry.caveat));
      document.body.append(pop);
      const r = s.getBoundingClientRect();
      const top = Math.min(window.innerHeight - pop.offsetHeight - 10, r.bottom + 8);
      pop.style.top = Math.max(8, top) + 'px';
      pop.style.left = Math.max(8, Math.min(window.innerWidth - pop.offsetWidth - 8, r.left)) + 'px';
      ev.stopPropagation();
    };
    s.addEventListener('click', show);
    s.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') show(e); });
    return s;
  }
  function hidePop() { if (pop) { pop.remove(); pop = null; } }
  document.addEventListener('click', e => { if (pop && !pop.contains(e.target)) hidePop(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') hidePop(); });

  /* ---------- poll (single question, remembered) ---------- */
  function renderPoll(container, cfg) {
    container.innerHTML = '';
    const key = cfg.key;
    const saved = store.get(key, null);
    const note = el('p', { class: 'small' });
    const opts = cfg.options.map(o => el('button', { class: 'opt' + (saved === o ? ' sel' : ''), onclick: () => { store.set(key, o); opts.forEach(x => x.classList.toggle('sel', x.textContent === o)); note.textContent = cfg.thanks || 'Remembered. You will meet this answer again at the end.'; if (cfg.onPick) cfg.onPick(o); } }, o));
    container.append(el('div', { class: 'lead', style: 'font-weight:650;color:var(--ink)' }, cfg.question), ...opts, note);
    if (saved) note.textContent = cfg.thanks || 'Remembered. You will meet this answer again at the end.';
  }

  /* ---------- journal box (remembered free text) ---------- */
  function journal(key, placeholder) {
    const t = el('textarea', { class: 'journal', placeholder: placeholder || 'Your own words…' });
    t.value = store.get(key, '');
    t.addEventListener('input', () => store.set(key, t.value));
    return t;
  }

  return { store, el, esc, $, nodata, lensBar, setLens, lens, sourceChip, quote, voiceTag, missingBadge, caveat, verseCard, renderVerseExplorer, renderTimeline, renderSortBins, renderFlipPairs, renderAccordion, renderStepper, glossaryTerm, renderPoll, journal };
})();
