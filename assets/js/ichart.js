/* assets/js/ichart.js: interactive charts for the site (prototype, Nov 2026).

   No library and no build step: plain SVG and DOM, one file, loaded only on pages that use the ichart
   shortcode. Each <figure class="ichart"> already holds, printed by Hugo, the static chart, the controls,
   the "how to read this" text, the numbers as a table and its data as JSON. This script draws the
   interactive plot into the stage (whose height CSS fixed before it ran) and wires the controls.
   If it fails or never loads, the static chart stays. */
const NS = "http://www.w3.org/2000/svg";
const svgEl = (name, attrs, parent) => {
  const e = document.createElementNS(NS, name);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
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

for (const fig of document.querySelectorAll("figure.ichart")) {
  try {
    const c = JSON.parse(fig.querySelector(".ichart-data").textContent);
    (c.type === "switch" ? switcher : timeline)(fig, c);
  } catch (err) {
    fig.classList.remove("is-live"); // leave the static chart in place
    console.error("ichart:", err);
  }
}
