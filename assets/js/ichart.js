/* assets/js/ichart.js: interactive charts for the site (prototype, Nov 2026).

   No library and no build step: plain SVG and DOM, one file, loaded only on pages that use the ichart
   shortcode. Each <figure class="ichart"> already holds, printed by Hugo, the static chart, the controls,
   the "how to read this" text, the numbers as a table and its data as JSON. This script draws the
   interactive plot into the stage (whose height CSS fixed before it ran) and wires the controls.
   If it fails or never loads, the static chart stays. */
const NS = "http://www.w3.org/2000/svg";
const setA = (e, attrs) => {
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  return e;
};
const svgEl = (name, attrs, parent) => {
  const e = setA(document.createElementNS(NS, name), attrs);
  if (parent) parent.appendChild(e);
  return e;
};
const htmlEl = (name, cls, parent, text) => {
  const e = document.createElement(name);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
};
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const num = (v, d) => Number(v).toLocaleString("en-SG", { minimumFractionDigits: d, maximumFractionDigits: d });

function timeline(fig, c) {
  const stage = fig.querySelector(".ichart-stage");
  const range = fig.querySelector("input[type=range]");
  const year = fig.querySelector(".ichart-year");
  const readout = fig.querySelector(".ichart-readout");
  const play = fig.querySelector(".ichart-play");
  const steps = [...fig.querySelectorAll("[data-step]")];
  const n = c.x.length;
  const svg = svgEl("svg", { "aria-hidden": "true", focusable: "false" }, stage);
  let idx = n - 1;
  let timer = null;
  let touched = false; // once the reader has used a control, the intro animation never starts

  function draw() {
    const W = stage.clientWidth, H = stage.clientHeight;
    if (!W || !H) return;
    const ph = H / c.panels.length;
    const m = { l: 30, r: 14, t: 30, b: 22 };
    const x = (i) => m.l + ((W - m.l - m.r) * i) / (n - 1);
    const gap = Math.max(2, Math.ceil(52 / ((W - m.l - m.r) / (n - 1)))); // year labels at least 52px apart
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.replaceChildren();
    c.panels.forEach((p, k) => {
      const top = k * ph;
      const multi = p.series.length > 1;
      const mt = multi ? m.t + 18 : m.t; // room for the legend row
      const y = (v) => top + mt + (ph - mt - m.b) * (1 - (v - p.domain[0]) / (p.domain[1] - p.domain[0]));
      svgEl("text", { x: 0, y: top + 14, class: "t-panel" }, svg).textContent = p.title;
      if (p.band) svgEl("rect", { x: m.l, y: y(p.band[1]), width: W - m.l - m.r, height: y(p.band[0]) - y(p.band[1]), class: "band" }, svg);
      p.ticks.forEach((t) => {
        svgEl("line", { x1: m.l, x2: W - m.r, y1: y(t), y2: y(t), class: t === p.baseline || t === 0 ? "base" : "grid" }, svg);
        svgEl("text", { x: m.l - 6, y: y(t) + 4, "text-anchor": "end" }, svg).textContent = t;
      });
      c.x.forEach((xv, i) => {
        if (i === 0 || i === n - 1 || (xv % 5 === 0 && i >= gap && i <= n - 1 - gap)) {
          svgEl("text", { x: x(i), y: top + ph - 6, "text-anchor": i === 0 ? "start" : i === n - 1 ? "end" : "middle" }, svg).textContent = xv;
        }
      });
      p.series.forEach((s) => {
        const pts = s.values.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`);
        svgEl("path", { d: "M" + pts.join("L"), class: `ghost ${s.role}` }, svg);
        svgEl("path", { d: "M" + pts.slice(0, idx + 1).join("L") + (idx === 0 ? "h0" : ""), class: `live ${s.role}` }, svg);
      });
      (p.mute || []).length && (() => {
        const a = c.x.indexOf(p.mute[0]), b = c.x.indexOf(p.mute[p.mute.length - 1]);
        if (a < 0 || b < 0) return;
        svgEl("rect", { x: x(a) - 6, y: top + mt, width: x(b) - x(a) + 12, height: ph - mt - m.b, class: "mute" }, svg);
      })();
      (p.flag || []).forEach((fy) => {
        const i = c.x.indexOf(fy);
        if (i >= 0) svgEl("circle", { cx: x(i), cy: y(p.series[0].values[i]), r: 7, class: "flag" }, svg);
      });
      svgEl("line", { x1: x(idx), x2: x(idx), y1: top + mt - 4, y2: top + ph - m.b, class: "cursor" }, svg);
      let lx = 0; // legend row: swatch, name and the value at the selected year, in one fixed place
      p.series.forEach((s) => {
        const v = s.values[idx];
        svgEl("circle", { cx: x(idx), cy: y(v), r: 5, class: `dot ${s.role}` }, svg);
        if (multi) {
          svgEl("line", { x1: lx, x2: lx + 14, y1: top + 28, y2: top + 28, class: `live ${s.role}` }, svg);
          const t = svgEl("text", { x: lx + 19, y: top + 32, class: "t-value" }, svg);
          t.textContent = `${s.label} ${num(v, p.decimals)}`;
          lx += 19 + t.getComputedTextLength() + 16;
        } else {
          const right = idx > n * 0.6;
          const above = y(v) - top > mt + 18;
          svgEl("text", { x: x(idx) + (right ? -9 : 9), y: y(v) + (above ? -10 : 19), "text-anchor": right ? "end" : "start", class: "t-value" }, svg)
            .textContent = `${num(v, p.decimals)} ${p.unit}`;
        }
      });
    });
  }

  function set(i, stepText) {
    idx = Math.max(0, Math.min(n - 1, i));
    range.value = idx;
    range.setAttribute("aria-valuetext", String(c.x[idx]));
    year.textContent = c.x[idx];
    if (stepText !== false) readout.textContent = stepText || c.notes[String(c.x[idx])] || "";
    if (!stepText) steps.forEach((b) => b.setAttribute("aria-pressed", "false"));
    draw();
  }
  function stop() {
    clearInterval(timer);
    timer = null;
    play.textContent = "Play";
    play.setAttribute("aria-pressed", "false");
  }
  function start(quiet) {
    if (idx >= n - 1) set(0, quiet ? false : undefined);
    play.textContent = "Pause";
    play.setAttribute("aria-pressed", "true");
    timer = setInterval(() => {
      if (quiet && touched) { stop(); return; } // the reader took over during the intro
      if (idx >= n - 1) { stop(); set(idx); return; }
      set(idx + 1, quiet ? false : undefined);
    }, quiet ? 70 : 480);
  }
  const fromPointer = (ev) => {
    const r = svg.getBoundingClientRect();
    const f = (ev.clientX - r.left - 30) / (r.width - 44);
    return Math.round(f * (n - 1));
  };
  fig.addEventListener("pointerdown", () => { touched = true; }, true);
  fig.addEventListener("keydown", () => { touched = true; }, true);
  svg.addEventListener("pointerdown", (ev) => { stop(); svg.setPointerCapture(ev.pointerId); set(fromPointer(ev)); });
  svg.addEventListener("pointermove", (ev) => {
    if (ev.pointerType === "mouse" || ev.buttons) { const i = fromPointer(ev); if (i !== idx && !timer) set(i); }
  });
  range.addEventListener("input", () => { stop(); set(Number(range.value)); });
  play.addEventListener("click", () => (timer ? stop() : start(false)));
  steps.forEach((b) => b.addEventListener("click", () => {
    touched = true;
    stop();
    const s = c.steps[Number(b.dataset.step)];
    set(c.x.indexOf(s.at), s.text);
    steps.forEach((o) => o.setAttribute("aria-pressed", o === b ? "true" : "false"));
  }));
  new ResizeObserver(draw).observe(stage);
  fig.classList.add("is-live");
  draw();
  // The line draws itself once, the first time the chart scrolls into view. The text does not change.
  if (!reduced && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { io.disconnect(); if (!timer && !touched) { set(0, false); start(true); } }
    }, { threshold: 0.6 });
    io.observe(stage);
  }
}

function switcher(fig, c) {
  const stage = fig.querySelector(".ichart-stage");
  const readout = fig.querySelector(".ichart-readout");
  const buttons = [...fig.querySelectorAll("[data-state]")];
  const [d0, d1] = c.domain;
  const pos = (v) => ((v - d0) / (d1 - d0)) * 100;
  const rows = htmlEl("div", "ic-rows", stage);
  rows.setAttribute("aria-hidden", "true");
  const kinds = ["partner", "subject", "pair"];
  const parts = kinds.map((kind) => {
    const row = htmlEl("div", "ic-row", rows);
    const label = htmlEl("div", "ic-row-label", row);
    const track = htmlEl("div", "ic-track", row);
    htmlEl("div", "ic-zero", track).style.left = pos(0) + "%";
    return { label, bar: htmlEl("div", "ic-bar " + kind, track), val: htmlEl("div", "ic-val", track) };
  });
  htmlEl("div", "ic-share-title", rows, "Share of the move (of the change in logs)");
  const share = htmlEl("div", "ic-share", rows);
  const segP = htmlEl("div", "partner", share), segS = htmlEl("div", "subject", share);
  const key = htmlEl("div", "ic-share-key", rows);
  const keyP = htmlEl("span", "k-partner", key), keyS = htmlEl("span", "k-subject", key);

  function set(i) {
    const s = c.states[i];
    s.bars.forEach(([label, v], j) => {
      const p = parts[j];
      p.label.textContent = label;
      p.bar.style.left = Math.min(pos(0), pos(v)) + "%";
      p.bar.style.width = Math.abs(pos(v) - pos(0)) + "%";
      p.val.textContent = (v > 0 ? "up " : "down ") + num(Math.abs(v), 1) + "%";
      const inside = pos(v) > 72; // a long bar carries its label inside its right end
      p.val.style.left = (v < 0 ? pos(0) : pos(v)) + "%";
      p.val.style.transform = inside ? "translateX(calc(-100% - 8px))" : "translateX(6px)";
    });
    segP.style.flexGrow = s.shares.sgd * 100;
    segS.style.flexGrow = s.shares.other * 100;
    keyP.textContent = `${c.partner} ${Math.round(s.shares.sgd * 100)}%`;
    keyS.textContent = `${c.subject} ${Math.round(s.shares.other * 100)}%`;
    const rem = Math.round(s.shares.remainder * 100);
    readout.textContent = s.explain + (rem ? ` The two shares sum to ${100 - rem}%; the remainder is ${rem}%.` : " The two shares sum to 100% exactly.");
    buttons.forEach((b, j) => b.setAttribute("aria-pressed", j === i ? "true" : "false"));
  }
  buttons.forEach((b) => b.addEventListener("click", () => set(Number(b.dataset.state))));
  fig.classList.add("is-live");
  set(0);
}

/* ---- Round two (Nov 2026): three bolder ways to read the same data ------------------------------------
   explain  tap a point and a card reads it in plain words
   compare  the reader picks the starting year; the chart answers against it
   panel    a dark instrument panel whose story steps advance as the reader scrolls
   Every number and every sentence shown is read from the chart's JSON, which tools/build_chart_data.py
   writes; nothing is worked out here except where to draw it. Numbers in between two years appear only
   while something is moving, and every movement ends on a number from the file. */
const $ = (el, sel) => el.querySelector(sel);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const newSvg = (parent) => svgEl("svg", { "aria-hidden": "true", focusable: "false" }, parent);
const icon = (name, parent) => svgEl("use", { href: "#ic-" + name }, svgEl("svg", { class: "ic-i", "aria-hidden": "true" }, parent));
const pressed = (buttons, on) => buttons.forEach((b, j) => b.setAttribute("aria-pressed", j === on ? "true" : "false"));
const pathOf = (vals, X, Y, a = 0, b = vals.length - 1) => {
  let d = "";
  for (let i = a; i <= b; i++) d += (i > a ? "L" : "M") + X(i).toFixed(1) + "," + Y(vals[i]).toFixed(1);
  return d;
};

// A number that moves a part of the way to its target on every frame, so a change glides instead of
// stepping. The rate is per 1/60 s, whatever the screen's frame rate. With reduced motion it jumps.
function chaser(cb, rate) {
  let cur = null, to = 0, raf = 0, r = rate, last = 0;
  const tick = (now) => {
    raf = 0;
    cur = Math.abs(to - cur) < 0.004 ? to : cur + (to - cur) * (1 - (1 - r) ** clamp((now - last) / 16.7, 0.5, 6));
    last = now;
    cb(cur);
    if (cur !== to) raf = requestAnimationFrame(tick);
  };
  return (v, jump, slow) => {
    to = v;
    r = slow || rate;
    if (cur === null || jump || reduced) { cur = v; cb(v); } else if (!raf) { last = performance.now(); raf = requestAnimationFrame(tick); }
  };
}

// The fixed parts of a line plot: target band, grid, year labels. Returns the two scales.
function plot(svg, stage, xs, p, m, fmt) {
  const W = stage.clientWidth, H = stage.clientHeight, n = xs.length, [d0, d1] = p.domain;
  if (!W || !H) return null;
  const X = (i) => m.l + ((W - m.l - m.r) * i) / (n - 1);
  const Y = (v) => m.t + (H - m.t - m.b) * (1 - (v - d0) / (d1 - d0));
  setA(svg, { viewBox: `0 0 ${W} ${H}` }).replaceChildren();
  if (p.band) svgEl("rect", { x: m.l, y: Y(p.band[1]), width: W - m.l - m.r, height: Y(p.band[0]) - Y(p.band[1]), class: "band" }, svg);
  p.ticks.forEach((t) => {
    svgEl("line", { x1: m.l, x2: W - m.r, y1: Y(t), y2: Y(t), class: t ? "grid" : "base" }, svg);
    svgEl("text", { x: m.l - 6, y: Y(t) + 4, "text-anchor": "end" }, svg).textContent = fmt ? fmt(t) : t;
  });
  const gap = Math.max(2, Math.ceil(52 / ((W - m.l - m.r) / (n - 1)))), years = [];
  xs.forEach((xv, i) => {
    if (i === 0 || i === n - 1 || (xv % 5 === 0 && i >= gap && i <= n - 1 - gap)) {
      const t = svgEl("text", { x: X(i), y: H - 6, "text-anchor": i === 0 ? "start" : i === n - 1 ? "end" : "middle" }, svg);
      t.textContent = xv;
      years.push([t, X(i) + (i === 0 ? 14 : i === n - 1 ? -14 : 0)]);
    }
  });
  if (p.mute) { // years the piece did not score are drawn faint
    const a = xs.indexOf(p.mute[0]), b = xs.indexOf(p.mute[p.mute.length - 1]);
    svgEl("rect", { x: X(a) - 6, y: m.t, width: X(b) - X(a) + 12, height: H - m.t - m.b, class: "mute" }, svg);
  }
  return { X, Y, W, H, years };
}

// Touch or drag on a plot picks the nearest year; with a mouse, moving over it is enough.
function scrub(svg, m, n, cb, hover) {
  const at = (ev) => {
    const r = svg.getBoundingClientRect();
    return clamp(Math.round(((ev.clientX - r.left - m.l) / (r.width - m.l - m.r)) * (n - 1)), 0, n - 1);
  };
  svg.addEventListener("pointerdown", (ev) => { svg.setPointerCapture(ev.pointerId); cb(at(ev)); });
  svg.addEventListener("pointermove", (ev) => { if (ev.buttons || (hover && ev.pointerType === "mouse")) cb(at(ev)); });
}

// The year under the selected point, as a filled label on the axis.
function pill(g, parts, x, text) {
  const px = clamp(x, 24, g.W - 24);
  (g.years || []).forEach(([t, tx]) => t.setAttribute("visibility", Math.abs(tx - px) < 42 ? "hidden" : "visible"));
  setA(parts[0], { x: px - 24, y: g.H - 21, width: 48, height: 20, rx: 10, class: "pill" });
  setA(parts[1], { x: px, y: g.H - 6, "text-anchor": "middle", class: "t-pill" }).textContent = text;
  return px;
}

/* A. Explain this point */
function explain(fig, c) {
  const stage = $(fig, ".ichart-stage"), range = $(fig, "input"), card = $(fig, ".ic-card"), year = $(fig, ".ic-year");
  const big = $(fig, ".ic-big b"), step = $(fig, ".ic-step"), lines = $(fig, ".ic-lines");
  const segs = [...fig.querySelectorAll("[data-series]")];
  const svg = newSvg(stage), n = c.x.length, m = { l: 30, r: 14, t: 14, b: 26 };
  let k = 0, idx = n - 1, g, dyn;
  const panelNow = () => c.panels[c.explain[k]];

  function place() {
    const v = panelNow().series[0].values[idx], x = g.X(idx), y = g.Y(v);
    setA(dyn.beam, { x1: x, x2: x, y1: y + 9, y2: g.H - 21 });
    setA(dyn.halo, { cx: x, cy: y });
    setA(dyn.dot, { cx: x, cy: y });
    card.style.setProperty("--ic-x", pill(g, dyn.pill, x, c.x[idx]) + "px");
  }
  function draw() {
    const p = panelNow(), vals = p.series[0].values, flag = p.flag || [];
    g = plot(svg, stage, c.x, p, m);
    if (!g) return;
    const d = pathOf(vals, g.X, g.Y);
    if (!p.domain[0]) { // an area is filled only where the axis starts at zero
      const lg = svgEl("linearGradient", { id: fig.id + "-g", x1: 0, y1: 0, x2: 0, y2: 1 }, svgEl("defs", {}, svg));
      svgEl("stop", { offset: 0, class: "g0" }, lg);
      svgEl("stop", { offset: 1, class: "g1" }, lg);
      svgEl("path", { d: `${d}L${g.X(n - 1)},${g.Y(0)}L${g.X(0)},${g.Y(0)}Z`, fill: `url(#${fig.id}-g)` }, svg);
    }
    svgEl("path", { d, class: "live subject" }, svg);
    vals.forEach((v, i) => {
      svgEl("circle", { cx: g.X(i), cy: g.Y(v), r: 2.5, class: "pt" }, svg);
      if (flag.includes(c.x[i])) svgEl("circle", { cx: g.X(i), cy: g.Y(v), r: 8, class: "flag" }, svg);
    });
    dyn = { beam: svgEl("line", { class: "beam" }, svg), halo: svgEl("circle", { r: 9, class: "halo" }, svg),
      dot: svgEl("circle", { r: 5.5, class: "dot subject" }, svg), pill: [svgEl("rect", {}, svg), svgEl("text", {}, svg)] };
    place();
  }
  function set(i, nk) {
    if (nk != null) { k = nk; pressed(segs, k); draw(); }
    idx = clamp(i, 0, n - 1);
    const pt = panelNow().points[idx];
    range.value = idx;
    range.setAttribute("aria-valuetext", c.x[idx]);
    year.textContent = c.x[idx];
    big.textContent = pt.big;
    step.dataset.dir = pt.dir;
    step.lastElementChild.textContent = pt.step;
    lines.replaceChildren();
    pt.lines.forEach(([ic, text]) => {
      const li = htmlEl("li", "", lines);
      icon(ic, li);
      htmlEl("span", "", li, text);
    });
    card.classList.remove("rise"); // the card rises again for each new point
    void card.offsetWidth;
    card.classList.add("rise");
    if (g) place();
  }
  scrub(svg, m, n, (i) => { if (i !== idx) set(i); }, true);
  range.addEventListener("input", () => set(Number(range.value)));
  $(fig, ".ic-prev").addEventListener("click", () => set(idx - 1));
  $(fig, ".ic-next").addEventListener("click", () => set(idx + 1));
  segs.forEach((b, j) => b.addEventListener("click", () => set(idx, j)));
  new ResizeObserver(draw).observe(stage);
  draw();
}

/* B. Build the comparison */
function compare(fig, c) {
  const q = c.compare, S = q.starts, n = c.x.length, m = { l: 40, r: 16, t: 14, b: 26 };
  const stage = $(fig, ".ichart-stage"), strip = $(fig, ".ic-strip"), range = $(fig, "input"), year = $(fig, ".ic-year");
  const bigP = $(fig, ".ic-big"), pct = $(fig, ".ic-pct"), head = $(fig, ".ic-headline"), text = $(fig, ".ic-text");
  const presets = [...fig.querySelectorAll("[data-start]")];
  const svg = newSvg(stage), bars = newSvg(strip);
  const sign = (v) => (v > 0 ? "+" : v < 0 ? "-" : "") + Math.abs(Math.round(v)) + "%";
  let s = q.initial, shown = S[s].values, from = shown, g, dyn;

  function paint(t) {
    if (!g) return;
    const o = S[s], y0 = g.Y(0), e = shown[n - 1], d = pathOf(shown, g.X, g.Y, s);
    const area = `${d}L${g.X(n - 1)},${y0}L${g.X(s)},${y0}Z`;
    setA(dyn.ghost, { d: pathOf(shown, g.X, g.Y, 0, s) });
    setA(dyn.up, { d: area });
    setA(dyn.down, { d: area });
    setA(dyn.line, { d });
    setA(dyn.start, { cx: g.X(s), cy: g.Y(shown[s]) });
    setA(dyn.end, { cx: g.X(n - 1), cy: g.Y(e) });
    setA(dyn.label, { x: g.X(n - 1) - 9, y: g.Y(e) + (e < 0 ? 19 : -10) }).textContent = t < 1 ? sign(e) : o.pct_text;
    pct.textContent = t < 1 ? sign(e) : o.pct_text;
    pill(g, dyn.pill, g.X(s), o.year);
  }
  const go = chaser((t) => { shown = from.map((v, i) => lerp(v, S[s].values[i], t)); paint(t); }, 0.2);

  function draw() {
    g = plot(svg, stage, c.x, q, m, sign);
    if (!g) return;
    const id = fig.id, y0 = g.Y(0), defs = svgEl("defs", {}, svg);
    svgEl("rect", { x: 0, y: 0, width: g.W, height: y0 }, svgEl("clipPath", { id: id + "-u" }, defs));
    svgEl("rect", { x: 0, y: y0, width: g.W, height: g.H }, svgEl("clipPath", { id: id + "-d" }, defs));
    svgEl("text", { x: g.W - m.r, y: m.t + 9, "text-anchor": "end", class: "t-up" }, svg).textContent = "more years of income";
    svgEl("text", { x: g.W - m.r, y: g.H - m.b - 5, "text-anchor": "end", class: "t-down" }, svg).textContent = "fewer years of income";
    dyn = { ghost: svgEl("path", { class: "ghost" }, svg),
      up: svgEl("path", { class: "area up", "clip-path": `url(#${id}-u)` }, svg),
      down: svgEl("path", { class: "area down", "clip-path": `url(#${id}-d)` }, svg),
      line: svgEl("path", { class: "live" }, svg),
      start: svgEl("circle", { r: 5, class: "pt" }, svg), end: svgEl("circle", { r: 5.5, class: "dot" }, svg),
      label: svgEl("text", { "text-anchor": "end", class: "t-value" }, svg), pill: [svgEl("rect", {}, svg), svgEl("text", {}, svg)] };
    paint(1);
  }
  // Every starting year at once: one bar each, up for "the last year is higher", down for "lower".
  function drawBars() {
    const W = strip.clientWidth, H = strip.clientHeight, [d0, d1] = q.strip_domain, bw = W / S.length;
    if (!W) return;
    const Y = (v) => 18 + (H - 40) * (1 - (v - d0) / (d1 - d0));
    setA(bars, { viewBox: `0 0 ${W} ${H}` }).replaceChildren();
    S.forEach((o, j) => {
      const y = Y(Math.max(0, o.pct)), cx = (j + 0.5) * bw, on = j === s;
      svgEl("rect", { x: j * bw + 3, y, width: bw - 6, height: Math.max(2, Math.abs(Y(o.pct) - Y(0))), rx: 3,
        class: (o.dir > 0 ? "up" : "down") + (on ? "" : " off") }, bars);
      if (on) svgEl("text", { x: cx, y: y - 5, "text-anchor": "middle", class: "t-value" }, bars).textContent = o.pct_text;
      if (on) pill({ W, H }, [svgEl("rect", {}, bars), svgEl("text", {}, bars)], cx, o.year);
      else if ((j === 0 || j === S.length - 1) && Math.abs(j - s) > 1) {
        svgEl("text", { x: j ? W : 0, y: H - 6, "text-anchor": j ? "end" : "start" }, bars).textContent = o.year;
      }
    });
    svgEl("line", { x1: 0, x2: W, y1: Y(0), y2: Y(0), class: "base" }, bars);
  }
  function set(j) {
    from = shown;
    s = clamp(j, 0, S.length - 1);
    const o = S[s];
    range.value = s;
    range.setAttribute("aria-valuetext", o.year);
    year.textContent = o.year;
    bigP.dataset.dir = o.dir;
    head.textContent = o.headline;
    text.textContent = o.verdict + " " + o.why;
    presets.forEach((b) => b.setAttribute("aria-pressed", Number(b.dataset.start) === s ? "true" : "false"));
    drawBars();
    go(0, true);
    go(1);
  }
  const pick = (j) => { if (j !== s) set(j); };
  scrub(svg, m, n, pick);
  scrub(bars, { l: strip.clientWidth / S.length / 2, r: strip.clientWidth / S.length / 2 }, S.length, pick);
  range.addEventListener("input", () => set(Number(range.value)));
  presets.forEach((b) => b.addEventListener("click", () => set(Number(b.dataset.start))));
  new ResizeObserver(() => { draw(); drawBars(); }).observe(stage);
  draw();
  drawBars();
}

/* C. Instrument panel */
function panel(fig, c) {
  const stage = $(fig, ".ichart-stage"), range = $(fig, "input"), year = $(fig, ".ic-year"), play = $(fig, ".ichart-play");
  const note = $(fig, ".ichart-readout"), dials = [...fig.querySelectorAll(".ic-dial")], steps = [...fig.querySelectorAll(".ic-story li")];
  const svg = newSvg(stage), n = c.x.length, m = { l: 30, r: 14, t: 26, b: 24 }, id = fig.id;
  let k = 0, idx = n - 1, pos = n - 1, g, dyn, timer = 0, stepOn = -1, intro = !reduced;

  // One dial for each kind of road: the whole arc is the axis, the thick part is the target band.
  const arcs = dials.map((b, j) => {
    const p = c.panels[j], [d0, d1] = p.domain, f = (v) => clamp((100 * (v - d0)) / (d1 - d0), 0, 100);
    const a = setA(newSvg($(b, ".ic-dial-arc")), { viewBox: "0 0 120 66" });
    const arc = (cls, dash) => svgEl("path", { d: "M10 60A50 50 0 0 1 110 60", pathLength: 100, class: cls, "stroke-dasharray": dash }, a);
    arc("arc-track", "none");
    arc("arc-band", `0 ${f(p.band[0])} ${f(p.band[1]) - f(p.band[0])} 200`);
    return { p, f, val: arc("arc-val", "0 200"), tip: svgEl("circle", { r: 4.5, class: "arc-tip" }, a),
      num: $(b, ".ic-dial-num"), status: $(b, ".ic-dial-status") };
  });

  function frame(at) {
    pos = at;
    const i0 = Math.floor(pos), i1 = Math.min(n - 1, i0 + 1), t = pos - i0;
    arcs.forEach((a, j) => {
      const vals = a.p.series[0].values, v = lerp(vals[i0], vals[i1], t), f = a.f(v), ang = Math.PI * (1 - f / 100);
      a.num.textContent = t ? num(v, 1) : vals[i0];
      setA(a.val, { "stroke-dasharray": `${f} 200` });
      setA(a.tip, { cx: 60 + 50 * Math.cos(ang), cy: 60 - 50 * Math.sin(ang) });
      if (j === k && g) {
        const x = lerp(g.X(i0), g.X(i1), t), y = g.Y(v);
        setA(dyn.clip, { width: x });
        setA(dyn.halo, { cx: x, cy: y });
        setA(dyn.dot, { cx: x, cy: y });
      }
    });
  }
  const go = chaser(frame, 0.17);

  function draw() {
    const p = c.panels[k], vals = p.series[0].values;
    g = plot(svg, stage, c.x, p, m);
    if (!g) return;
    const d = pathOf(vals, g.X, g.Y);
    svgEl("text", { x: 0, y: 13, class: "t-panel" }, svg).textContent = p.title;
    dyn = { clip: svgEl("rect", { x: 0, y: 0, height: g.H }, svgEl("clipPath", { id: id + "-c" }, svgEl("defs", {}, svg))) };
    svgEl("path", { d, class: "ghost subject" }, svg);
    svgEl("path", { d, class: "live subject", "clip-path": `url(#${id}-c)` }, svg);
    (p.flag || []).forEach((fy) => {
      const i = c.x.indexOf(fy);
      svgEl("circle", { cx: g.X(i), cy: g.Y(vals[i]), r: 8, class: "flag" }, svg);
    });
    dyn.halo = svgEl("circle", { r: 10, class: "halo" }, svg);
    dyn.dot = svgEl("circle", { r: 5.5, class: "dot subject" }, svg);
    frame(pos);
  }
  function set(i, nk, slow) {
    if (nk != null && nk !== k) { k = nk; pressed(dials, k); draw(); }
    idx = clamp(i, 0, n - 1);
    range.value = idx;
    range.setAttribute("aria-valuetext", c.x[idx]);
    year.textContent = c.x[idx];
    note.textContent = c.notes[c.x[idx]];
    arcs.forEach((a) => {
      a.status.textContent = a.p.status[idx];
      a.status.dataset.out = /above|below/.test(a.p.status[idx]) ? 1 : 0;
    });
    go(idx, false, slow);
  }
  function playing(on) {
    clearInterval(timer);
    timer = on ? setInterval(() => (idx >= n - 1 ? playing(false) : set(idx + 1)), 560) : 0;
    $(play, "use").setAttribute("href", on ? "#ic-pause" : "#ic-play");
    play.lastElementChild.textContent = on ? "Pause" : "Play";
    play.setAttribute("aria-pressed", on ? "true" : "false");
  }
  // The story: the last step whose top has come up past the lower part of the screen is the active one.
  function onScroll() {
    const r = fig.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    let a = -1;
    steps.forEach((li, j) => { if (li.getBoundingClientRect().top < innerHeight * 0.86) a = j; });
    if (a === stepOn) return;
    stepOn = a;
    steps.forEach((li, j) => li.classList.toggle("on", j === a));
    if (a >= 0) { playing(false); set(c.x.indexOf(c.steps[a].at), c.steps[a].panel); }
  }
  fig.addEventListener("pointerdown", () => { intro = false; }, true);
  fig.addEventListener("keydown", () => { intro = false; }, true);
  scrub(svg, m, n, (i) => { playing(false); if (i !== idx) set(i); });
  range.addEventListener("input", () => { playing(false); set(Number(range.value)); });
  play.addEventListener("click", () => { if (timer) playing(false); else { if (idx >= n - 1) set(0); playing(true); } });
  dials.forEach((b, j) => b.addEventListener("click", () => set(idx, j)));
  addEventListener("scroll", onScroll, { passive: true });
  new ResizeObserver(draw).observe(stage);
  draw();
  // The first time the panel is seen, the line draws itself and the numbers run up to the last year.
  new IntersectionObserver((entries, io) => {
    if (!entries.some((e) => e.isIntersecting)) return;
    io.disconnect();
    if (intro && stepOn < 0) { go(0, true); go(idx, false, 0.045); }
  }, { threshold: 0.6 }).observe(stage);
}

const MODES = { explain, compare, panel };
for (const fig of document.querySelectorAll("figure.ichart")) {
  try {
    const c = JSON.parse(document.getElementById(fig.dataset.chart).textContent);
    (MODES[fig.dataset.mode] || (c.type === "switch" ? switcher : timeline))(fig, c);
    fig.classList.add("is-live");
  } catch (err) {
    fig.classList.remove("is-live"); // leave the static chart in place
    console.error("ichart:", err);
  }
}
