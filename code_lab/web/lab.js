// The Code Lab front-end.
// Loads lessons, builds knobs for the variables, runs the child's Python on the
// local server, and draws/plays/animates whatever comes back — across five
// tracks: Draw, Music, Maze, Move (animation), and Play (interactive).

const codeEl     = document.getElementById("code");
const hlEl       = document.getElementById("code-highlight");
const gutterEl   = document.getElementById("gutter");
const knobsEl    = document.getElementById("knobs");
const statusEl   = document.getElementById("status");
const consoleEl  = document.getElementById("console");
const lessonsEl  = document.getElementById("lessons");
const goalEl     = document.getElementById("goal");
const tipBodyEl  = document.getElementById("tip-body");
const autorunEl  = document.getElementById("autorun");
const progressEl = document.getElementById("progress");
const progressBar = document.getElementById("progress-bar");
const canvas     = document.getElementById("stage");
const ctx        = canvas.getContext("2d");
const W = canvas.width, H = canvas.height;
const speakBtn = document.getElementById("speak");
const saveBtn  = document.getElementById("save");
const calmEl   = document.getElementById("calm");
const starsEl  = document.getElementById("stars");
const paletteEl = document.getElementById("palette");
const dpadEl   = document.getElementById("dpad");
const darkEl   = document.getElementById("dark");
const optionsBtn = document.getElementById("optionsBtn");
const optionsPanel = document.getElementById("optionsPanel");
const resetStarsBtn = document.getElementById("resetStars");
let errorShown = false;

let LESSONS = [];
let currentIndex = 0;
let currentBg = "#fff";

const COLORS = [
  "red", "orange", "gold", "yellow", "green", "limegreen", "teal",
  "deepskyblue", "blue", "navy", "purple", "violet", "magenta",
  "deeppink", "hotpink", "pink", "cyan", "saddlebrown", "brown",
  "black", "gray", "white",
];

// ===========================================================================
// Remembering things in the browser + read-aloud + calm mode + save picture.
// ===========================================================================
function lsGet(key, fallback) {
  try { const v = localStorage.getItem("codelab:" + key); return v === null ? fallback : JSON.parse(v); }
  catch (e) { return fallback; }
}
function lsSet(key, value) {
  try { localStorage.setItem("codelab:" + key, JSON.stringify(value)); } catch (e) {}
}
function lessonKey(les) { return (les.track || "") + "::" + (les.title || ""); }
function saveCode() { lsSet("code::" + lessonKey(currentLesson()), codeEl.value); }

let doneSet = lsGet("done", []);
function isDone(les) { return doneSet.indexOf(lessonKey(les)) !== -1; }
function markDone(les) {
  const k = lessonKey(les);
  if (doneSet.indexOf(k) === -1) { doneSet.push(k); lsSet("done", doneSet); }
  refreshStars();
}
function refreshStars() {
  starsEl.textContent = "⭐ " + doneSet.length + "/" + LESSONS.length;
  Array.from(lessonsEl.options).forEach((opt) => {
    const les = LESSONS[Number(opt.value)];
    if (!les) return;
    opt.textContent = (isDone(les) ? "⭐ " : "") + (les.emoji ? les.emoji + " " : "") + les.title;
  });
}

// Calm mode: fewer animations & sounds (auto-on if the OS asks for reduced motion).
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
calmEl.checked = lsGet("calm", false);
calmEl.addEventListener("change", () => lsSet("calm", calmEl.checked));
function calmMode() { return calmEl.checked || reduceMotion.matches; }

// Dark mode (the inline script in index.html applies it early to avoid a flash).
function applyDark(on) { document.body.classList.toggle("dark", on); }
darkEl.checked = lsGet("dark", false);
applyDark(darkEl.checked);
darkEl.addEventListener("change", () => { applyDark(darkEl.checked); lsSet("dark", darkEl.checked); });

// The ⚙️ Options menu: open/close (click outside or Esc closes it).
function setMenu(open) {
  optionsPanel.hidden = !open;
  optionsBtn.setAttribute("aria-expanded", open ? "true" : "false");
}
optionsBtn.addEventListener("click", (e) => { e.stopPropagation(); setMenu(optionsPanel.hidden); });
document.addEventListener("click", (e) => {
  if (!optionsPanel.hidden && !e.target.closest(".options")) setMenu(false);
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

// Clear all stars and start fresh.
resetStarsBtn.addEventListener("click", () => {
  if (window.confirm("Clear all your ⭐ stars and start fresh?")) {
    doneSet = [];
    lsSet("done", []);
    refreshStars();
  }
});

// Read the goal out loud (uses the browser's built-in voice).
function speakGoal() {
  if (!("speechSynthesis" in window)) return;
  const text = (currentLesson().goal || "").trim();
  if (!text) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.rate = 0.95; u.pitch = 1.05; u.lang = "en-US";
  window.speechSynthesis.speak(u);
}
speakBtn.addEventListener("click", speakGoal);

// Save the picture as a PNG (painting its background colour in first).
saveBtn.addEventListener("click", () => {
  const out = document.createElement("canvas");
  out.width = W; out.height = H;
  const octx = out.getContext("2d");
  octx.fillStyle = currentBg || "#fff";
  octx.fillRect(0, 0, W, H);
  octx.drawImage(canvas, 0, 0);
  const link = document.createElement("a");
  link.download = "my-code-lab-picture.png";
  link.href = out.toDataURL("image/png");
  link.click();
});

// ---- command palette: tap a chip to add a real line of code (no typing) ----
function findVar(code, ctorRegex, fallback) {
  const m = code.match(new RegExp("(\\w+)\\s*=\\s*" + ctorRegex));
  return m ? m[1] : fallback;
}
function buildPalette() {
  paletteEl.innerHTML = "";
  const code = codeEl.value;
  const track = currentLesson().track || "";
  let chips = [];
  if (track.indexOf("Draw") >= 0) {
    const t = findVar(code, "Turtle\\(", "t");
    chips = [["▶ forward", t + ".forward(100)"], ["↻ right", t + ".right(90)"],
             ["↺ left", t + ".left(90)"], ["🎨 color", t + '.color("red")'],
             ["⭕ circle", t + ".circle(60)"], ["• dot", t + '.dot(30, "gold")']];
  } else if (track.indexOf("Music") >= 0) {
    const s = findVar(code, "Song\\(", "song");
    chips = [["🎵 play C", s + '.play("C", 1)'], ["🎵 play G", s + '.play("G", 1)'],
             ["🤫 rest", s + ".rest(1)"]];
  } else if (track.indexOf("Maze") >= 0) {
    const r = findVar(code, "Robot\\(", "robot");
    chips = [["▶ forward", r + ".forward(1)"], ["↻ right", r + ".right()"], ["↺ left", r + ".left()"]];
  } else if (track.indexOf("Move") >= 0) {
    const stage = findVar(code, "Stage\\(", "stage");
    const m = code.match(/(\w+)\s*=\s*\w+\.add\(/);
    const sp = m ? m[1] : "hero";
    chips = [["→ right", sp + ".move(20, 0)"], ["↑ up", sp + ".move(0, 20)"],
             ["🔎 grow", sp + ".grow(10)"], ["➕ character", stage + '.add("🐶", 0, 0)']];
  } else {
    return;   // the Play track is function-based — no simple chips
  }
  const label = document.createElement("span");
  label.className = "palette-label";
  label.textContent = "➕ Add:";
  paletteEl.appendChild(label);
  chips.forEach(([text, snippet]) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = text;
    b.addEventListener("click", () => insertSnippet(snippet));
    paletteEl.appendChild(b);
  });
}
function insertSnippet(snippet) {
  codeEl.value = codeEl.value.replace(/\s+$/, "") + "\n" + snippet + "\n";
  syncHighlight();
  buildKnobs();
  saveCode();
  run(true);   // show what the new command did, right away
}

// ---- on-screen arrows for the Play track (so a tablet needs no keyboard) ----
dpadEl.querySelectorAll("button").forEach((b) => {
  b.addEventListener("click", () => sendEvent({ type: "key", key: b.dataset.key }));
});

// ===========================================================================
// Load lessons and fill the dropdown (grouped by track).
// ===========================================================================
fetch("/lessons")
  .then(r => r.json())
  .then(list => {
    LESSONS = list;
    let group = null, groupName = null;
    list.forEach((les, i) => {
      if (les.track !== groupName) {
        groupName = les.track;
        group = document.createElement("optgroup");
        group.label = les.track;
        lessonsEl.appendChild(group);
      }
      const opt = document.createElement("option");
      opt.value = i;
      opt.textContent = (les.emoji ? les.emoji + " " : "") + les.title;
      group.appendChild(opt);
    });
    refreshStars();
    const lastKey = lsGet("last", null);
    let startIdx = 0;
    if (lastKey) {
      const idx = LESSONS.findIndex(le => lessonKey(le) === lastKey);
      if (idx >= 0) startIdx = idx;
    }
    loadLesson(startIdx);
  })
  .catch(() => { statusEl.textContent = "Could not reach the Code Lab server."; });

function currentLesson() { return LESSONS[currentIndex] || {}; }

function loadLesson(i) {
  currentIndex = i;
  lessonsEl.value = i;
  const les = LESSONS[i];
  const saved = lsGet("code::" + lessonKey(les), null);
  codeEl.value = (saved !== null) ? saved : les.code;
  goalEl.textContent = (les.emoji ? les.emoji + "  " : "") + (les.goal || "");
  tipBodyEl.textContent = les.tip || "";
  lsSet("last", lessonKey(les));
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
  syncHighlight();
  buildKnobs();
  buildPalette();
  run(false);
}

lessonsEl.addEventListener("change", () => loadLesson(Number(lessonsEl.value)));
document.getElementById("next").addEventListener("click", () => loadLesson((currentIndex + 1) % LESSONS.length));
document.getElementById("reset").addEventListener("click", () => {
  lsSet("code::" + lessonKey(LESSONS[currentIndex]), null);   // forget my edits, restore the starter
  loadLesson(currentIndex);
});
document.getElementById("run").addEventListener("click", () => { buildKnobs(); buildPalette(); run(true); });
codeEl.addEventListener("change", () => { buildKnobs(); buildPalette(); saveCode(); });
codeEl.addEventListener("input", syncHighlight);
codeEl.addEventListener("scroll", () => {
  hlEl.scrollTop = codeEl.scrollTop;
  hlEl.scrollLeft = codeEl.scrollLeft;
  gutterEl.scrollTop = codeEl.scrollTop;
});

// Press Enter / Return anywhere to Run — except while typing in the code box.
document.addEventListener("keydown", (e) => {
  if (e.key !== "Enter" || e.shiftKey) return;
  if (document.activeElement && document.activeElement.id === "code") return;
  e.preventDefault();
  run(true);
});

// ===========================================================================
// Highlight layer + line numbers (so kids see which code a knob changes).
// ===========================================================================
function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function renderHighlight(name) {
  const lines = codeEl.value.split("\n");
  let target = -1;
  if (name) {
    const re = new RegExp("^" + name + "\\s*=");
    for (let i = 0; i < lines.length; i++) {
      if (re.test(lines[i])) { target = i; break; }
    }
  }
  hlEl.innerHTML = lines.map((line, i) => {
    const safe = escapeHtml(line) || " ";
    return i === target ? "<mark>" + safe + "</mark>" : safe;
  }).join("\n");
  hlEl.scrollTop = codeEl.scrollTop;
  hlEl.scrollLeft = codeEl.scrollLeft;
}
function syncHighlight() { errorShown = false; renderHighlight(null); updateGutter(); }
function renderErrorLine(lineNo) {
  const lines = codeEl.value.split("\n");
  hlEl.innerHTML = lines.map((line, i) => {
    const safe = escapeHtml(line) || " ";
    return (i === lineNo - 1) ? '<mark class="err">' + safe + "</mark>" : safe;
  }).join("\n");
  hlEl.scrollTop = codeEl.scrollTop;
  hlEl.scrollLeft = codeEl.scrollLeft;
  errorShown = true;
}
function updateGutter() {
  const count = codeEl.value.split("\n").length;
  let nums = "";
  for (let n = 1; n <= count; n++) nums += n + "\n";
  gutterEl.textContent = nums;
  gutterEl.scrollTop = codeEl.scrollTop;
}
let flashTimer = null;
function flashVariable(name, labelEl) {
  renderHighlight(name);
  if (labelEl) {
    labelEl.classList.remove("flash");
    void labelEl.offsetWidth;
    labelEl.classList.add("flash");
  }
  if (flashTimer) clearTimeout(flashTimer);
  flashTimer = setTimeout(syncHighlight, 1400);
}

// ===========================================================================
// Knobs: a control for each simple "name = value" line at the top of the code.
// ===========================================================================
function scanKnobs(code) {
  const knobs = [];
  const seen = new Set();
  for (const line of code.split("\n")) {
    const numM = line.match(/^([A-Za-z_]\w*)\s*=\s*(-?\d+(?:\.\d+)?)\s*(?:#.*)?$/);
    const strM = line.match(/^([A-Za-z_]\w*)\s*=\s*"([^"]*)"\s*(?:#.*)?$/);
    if (numM && !seen.has(numM[1])) {
      seen.add(numM[1]);
      knobs.push({ name: numM[1], type: "number",
                   value: parseFloat(numM[2]), isFloat: numM[2].includes(".") });
    } else if (strM && !seen.has(strM[1])) {
      seen.add(strM[1]);
      knobs.push({ name: strM[1], type: "string", value: strM[2] });
    }
  }
  return knobs;
}
function buildKnobs() {
  knobsEl.innerHTML = "";
  for (const knob of scanKnobs(codeEl.value)) {
    knobsEl.appendChild(knob.type === "number" ? numberKnob(knob) : stringKnob(knob));
  }
}
function numberKnob(knob) {
  const wrap = document.createElement("div"); wrap.className = "knob";
  const head = document.createElement("div"); head.className = "knob-head";
  const name = document.createElement("span"); name.className = "knob-name"; name.textContent = knob.name;
  const val = document.createElement("span"); val.className = "knob-val"; val.textContent = knob.value;
  head.append(name, val);
  const slider = document.createElement("input");
  slider.type = "range";
  const big = Math.abs(knob.value) > 1000;
  slider.min = big ? knob.value : Math.min(1, knob.value);
  slider.max = big ? knob.value : Math.max(knob.value * 3, knob.value + 12, 20);
  slider.step = knob.isFloat ? 0.1 : 1;
  slider.value = knob.value;
  slider.addEventListener("input", () => {
    const v = knob.isFloat ? parseFloat(slider.value) : parseInt(slider.value, 10);
    val.textContent = v;
    setVariable(knob.name, String(v));
    flashVariable(knob.name, name);
  });
  slider.addEventListener("change", () => { if (autorunEl.checked) run(true); });
  wrap.append(head, slider);
  return wrap;
}
function stringKnob(knob) {
  const wrap = document.createElement("div"); wrap.className = "knob";
  const head = document.createElement("div"); head.className = "knob-head";
  const name = document.createElement("span"); name.className = "knob-name"; name.textContent = knob.name;
  head.append(name);
  let control;
  const looksLikeColor = COLORS.includes(knob.value) ||
    /^#[0-9a-fA-F]{3,6}$/.test(knob.value) || knob.name.includes("color");
  if (looksLikeColor) {
    control = document.createElement("select");
    const options = COLORS.includes(knob.value) ? COLORS : [knob.value, ...COLORS];
    for (const c of options) {
      const o = document.createElement("option"); o.value = c; o.textContent = c; control.appendChild(o);
    }
    control.value = knob.value;
  } else {
    control = document.createElement("input"); control.type = "text"; control.value = knob.value;
  }
  control.addEventListener("input", () => {
    setVariable(knob.name, '"' + control.value + '"');
    flashVariable(knob.name, name);
  });
  control.addEventListener("change", () => {
    setVariable(knob.name, '"' + control.value + '"');
    flashVariable(knob.name, name);
    if (autorunEl.checked) run(true);
  });
  wrap.append(head, control);
  return wrap;
}
function setVariable(name, newValue) {
  const re = new RegExp("^(" + name + "\\s*=\\s*)([^#\\n]*?)(\\s*#.*)?$");
  const lines = codeEl.value.split("\n");
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(re);
    if (m) { lines[i] = m[1] + newValue + (m[3] || ""); break; }
  }
  codeEl.value = lines.join("\n");
}

// ===========================================================================
// RUN: send the code to the server, then show the result for its track.
// ===========================================================================
function setProgress(frac) { progressBar.style.width = Math.max(0, Math.min(1, frac)) * 100 + "%"; }

// ----- celebrating success -----------------------------------------------
// Every finish gives the message a happy "pop". A real win (solving a maze)
// also gets confetti + a cheerful chime.
let confettiId = null;
let celebrateRun = false;        // did the CHILD start this run? (not the auto-run on load)
function cheer(message, opts) {
  opts = opts || {};
  setProgress(1);
  progressEl.classList.add("done");
  statusEl.textContent = message;
  if (!celebrateRun) return;            // lesson just auto-loaded — show result, no party
  goalEl.classList.add("solved");       // the goal banner turns GREEN
  markDone(currentLesson());            // earn a ⭐ for this lesson
  if (calmMode()) return;               // calm mode: green + star, but no confetti/pop/chime
  statusEl.classList.remove("celebrate");
  void statusEl.offsetWidth;            // restart the pop animation
  statusEl.classList.add("celebrate");
  confetti();
  if (opts.chime) chime();
}
function confetti() {
  if (confettiId) cancelAnimationFrame(confettiId);
  const snapshot = ctx.getImageData(0, 0, W, H);   // keep the finished picture underneath
  const colors = ["#ff7aa2", "#ffd166", "#06d6a0", "#4cc9f0", "#9b5de5", "#ff9e00"];
  const pieces = [];
  for (let i = 0; i < 120; i++) {
    pieces.push({
      x: Math.random() * W, y: -20 - Math.random() * H * 0.5,
      vx: (Math.random() - 0.5) * 3, vy: 2.5 + Math.random() * 3.5,
      size: 6 + Math.random() * 8, color: colors[i % colors.length],
      rot: Math.random() * Math.PI, vr: (Math.random() - 0.5) * 0.3,
    });
  }
  const start = performance.now(), DURATION = 1600;
  function frame(now) {
    const elapsed = now - start;
    ctx.putImageData(snapshot, 0, 0);    // restore the picture, then confetti on top
    for (const p of pieces) {
      p.x += p.vx; p.y += p.vy; p.vy += 0.045; p.rot += p.vr;
      ctx.save();
      ctx.translate(p.x, p.y); ctx.rotate(p.rot);
      ctx.globalAlpha = Math.max(0, 1 - elapsed / DURATION);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
      ctx.restore();
    }
    if (elapsed < DURATION) confettiId = requestAnimationFrame(frame);
    else { confettiId = null; ctx.putImageData(snapshot, 0, 0); }
  }
  confettiId = requestAnimationFrame(frame);
}
function chime() {
  ensureAudio(); audioCtx.resume();
  const notes = [523.25, 659.25, 783.99, 1046.5];   // C5 E5 G5 C6 — a happy little run
  let t = audioCtx.currentTime;
  for (const f of notes) {
    const osc = audioCtx.createOscillator(), g = audioCtx.createGain();
    osc.type = "triangle"; osc.frequency.value = f;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(0.25, t + 0.02);
    g.gain.linearRampToValueAtTime(0, t + 0.18);
    osc.connect(g).connect(audioCtx.destination);
    osc.start(t); osc.stop(t + 0.2); musicNodes.push(osc);
    t += 0.1;
  }
}

function run(userInitiated) {
  celebrateRun = !!userInitiated;
  stopEverything();
  saveCode();
  goalEl.classList.remove("solved");
  statusEl.textContent = "Working...";
  consoleEl.className = "";
  consoleEl.textContent = "";
  fetch("/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: codeEl.value }),
  })
    .then(r => r.json())
    .then(result => {
      consoleEl.textContent = (result.output || "").replace(/\s+$/g, "");
      if (!result.ok && result.error) {
        const e = result.error;
        const msg = e.friendly || (e.type + ": " + e.message);
        const detail = e.line ? ("  (line " + e.line + ")") : "";
        consoleEl.textContent += (consoleEl.textContent ? "\n" : "") + "🤔 " + msg + detail;
        consoleEl.className = "error";
        statusEl.textContent = "🤔 Let's fix it!";
        if (e.line) renderErrorLine(e.line);
        ctx.clearRect(0, 0, W, H);
        setProgress(0); progressEl.classList.remove("done");
        return;
      }
      if (errorShown) syncHighlight();    // clear a previous red error line
      currentBg = result.background || "#fff";
      canvas.style.background = currentBg;
      progressEl.classList.remove("done"); setProgress(0);
      switch (result.kind) {
        case "music": musicRender(result.notes, result.bpm); break;
        case "maze":  mazeRender(result.commands, currentLesson().maze); break;
        case "anim":  animRender(result.frames); break;
        case "interactive": interactiveRender(result); break;
        default:      animate(result.ops || []);
      }
    })
    .catch(() => { statusEl.textContent = "Could not reach the server."; });
}

// Things that may be running between turns — cancel them before a new run.
let animId = null, mazeTimer = null;
let musicTimers = [], musicNodes = [], audioCtx = null;
let interactiveKey = null, interactiveClick = null, currentSid = null;

function stopEverything() {
  if (animId) { cancelAnimationFrame(animId); animId = null; }
  if (confettiId) { cancelAnimationFrame(confettiId); confettiId = null; }
  statusEl.classList.remove("celebrate");
  if (mazeTimer) { clearTimeout(mazeTimer); mazeTimer = null; }
  musicTimers.forEach(clearTimeout); musicTimers = [];
  musicNodes.forEach(n => { try { n.stop(); } catch (e) {} }); musicNodes = [];
  if (interactiveKey) { canvas.removeEventListener("keydown", interactiveKey); interactiveKey = null; }
  if (interactiveClick) { canvas.removeEventListener("click", interactiveClick); interactiveClick = null; }
  dpadEl.hidden = true;
  currentSid = null;
}

// ===========================================================================
// 🎨 DRAW renderer — the turtle draws step by step.
// ===========================================================================
function animate(ops) {
  if (ops.length === 0) { statusEl.textContent = "(nothing drawn yet)"; return; }
  const fit = computeFit(ops);
  const tx = x => W / 2 + (x - fit.cx) * fit.scale;
  const ty = y => H / 2 - (y - fit.cy) * fit.scale;
  const drawn = ops.filter(o => o.type === "line").length || 1;
  const perStep = Math.max(10, Math.min(220, 3600 / drawn));
  let i = 0, stepStart = null;
  function commit(upto) {
    ctx.clearRect(0, 0, W, H);
    for (let k = 0; k < upto; k++) drawOp(ops[k], tx, ty, fit.scale);
  }
  function frame(now) {
    if (stepStart === null) stepStart = now;
    if (i >= ops.length) {
      const last = ops[ops.length - 1];
      drawTurtle(tx(last.type === "dot" ? last.x : last.x2), ty(last.type === "dot" ? last.y : last.y2));
      cheer("🎉 You did it!");
      animId = null; return;
    }
    const op = ops[i];
    if (op.type === "dot") {
      drawOp(op, tx, ty, fit.scale);
      i++; stepStart = now; setProgress(i / ops.length);
      animId = requestAnimationFrame(frame); return;
    }
    const t = Math.min(1, (now - stepStart) / perStep);
    const cx = op.x1 + (op.x2 - op.x1) * t;
    const cy = op.y1 + (op.y2 - op.y1) * t;
    commit(i);
    if (op.type === "line") {
      ctx.beginPath();
      ctx.strokeStyle = op.color; ctx.lineWidth = Math.max(1, op.width * fit.scale);
      ctx.lineCap = "round";
      ctx.moveTo(tx(op.x1), ty(op.y1)); ctx.lineTo(tx(cx), ty(cy)); ctx.stroke();
    }
    drawTurtle(tx(cx), ty(cy));
    setProgress((i + t) / ops.length);
    if (t >= 1) { i++; stepStart = now; }
    animId = requestAnimationFrame(frame);
  }
  animId = requestAnimationFrame(frame);
}
function drawOp(op, tx, ty, scale) {
  if (op.type === "line") {
    ctx.beginPath();
    ctx.strokeStyle = op.color; ctx.lineWidth = Math.max(1, op.width * scale);
    ctx.lineCap = "round";
    ctx.moveTo(tx(op.x1), ty(op.y1)); ctx.lineTo(tx(op.x2), ty(op.y2)); ctx.stroke();
  } else if (op.type === "dot") {
    ctx.beginPath(); ctx.fillStyle = op.color;
    ctx.arc(tx(op.x), ty(op.y), Math.max(2, op.r * scale), 0, Math.PI * 2); ctx.fill();
  }
}
function drawTurtle(x, y) {
  ctx.save(); ctx.font = "24px serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillText("🐢", x, y); ctx.restore();
}
function computeFit(ops) {
  let minX, maxX, minY, maxY, found = false;
  for (const op of ops) {
    const pts = op.type === "dot" ? [[op.x, op.y]] : [[op.x1, op.y1], [op.x2, op.y2]];
    for (const [px, py] of pts) {
      if (!found) { minX = maxX = px; minY = maxY = py; found = true; }
      minX = Math.min(minX, px); maxX = Math.max(maxX, px);
      minY = Math.min(minY, py); maxY = Math.max(maxY, py);
    }
  }
  if (!found) { minX = maxX = minY = maxY = 0; }
  const pad = 50;
  let scale = Math.min((W - 2 * pad) / ((maxX - minX) || 1), (H - 2 * pad) / ((maxY - minY) || 1));
  if (!isFinite(scale) || scale <= 0) scale = 1;
  scale = Math.min(scale, 3);
  return { scale, cx: (minX + maxX) / 2, cy: (minY + maxY) / 2 };
}

// ===========================================================================
// 🎵 MUSIC renderer — plays the notes and shows them as bouncing bubbles.
// ===========================================================================
function ensureAudio() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return audioCtx;
}
function musicRender(notes, bpm) {
  if (!notes.length) { statusEl.textContent = "(no notes yet)"; return; }
  ensureAudio(); audioCtx.resume();
  const beat = 60 / bpm;
  let when = audioCtx.currentTime + 0.08;
  const offsets = [];
  for (const n of notes) {
    const dur = n.beats * beat;
    if (n.freq > 0) {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "triangle";
      osc.frequency.value = n.freq;
      const atk = 0.02, rel = 0.08;
      gain.gain.setValueAtTime(0, when);
      gain.gain.linearRampToValueAtTime(0.25, when + atk);
      gain.gain.setValueAtTime(0.25, when + Math.max(atk, dur - rel));
      gain.gain.linearRampToValueAtTime(0, when + dur);
      osc.connect(gain).connect(audioCtx.destination);
      osc.start(when); osc.stop(when + dur + 0.03);
      musicNodes.push(osc);
    }
    offsets.push(when - audioCtx.currentTime);
    when += dur;
  }
  const total = when - audioCtx.currentTime;
  drawMusic(notes, -1);
  notes.forEach((n, i) => {
    musicTimers.push(setTimeout(() => { drawMusic(notes, i); setProgress((i + 1) / notes.length); }, offsets[i] * 1000));
  });
  musicTimers.push(setTimeout(() => {
    drawMusic(notes, -1);
    cheer("🎉 You did it!");
  }, total * 1000 + 60));
  statusEl.textContent = "Playing... 🎵";
}
function drawMusic(notes, current) {
  ctx.clearRect(0, 0, W, H);
  const n = notes.length || 1;
  const gap = W / (n + 1);
  const freqs = notes.filter(x => x.freq > 0).map(x => x.freq);
  const lo = Math.min(261, ...freqs), hi = Math.max(523, ...freqs);
  notes.forEach((nt, i) => {
    const x = gap * (i + 1);
    let y = H / 2;
    if (nt.freq > 0) { const t = (nt.freq - lo) / ((hi - lo) || 1); y = H * 0.8 - t * H * 0.58; }
    const r = i === current ? 26 : 17;
    ctx.beginPath();
    ctx.fillStyle = nt.freq > 0 ? (i === current ? "#ff7aa2" : "#9b5de5") : "#d9d2ec";
    ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    if (i === current) { ctx.lineWidth = 4; ctx.strokeStyle = "#ffd166"; ctx.stroke(); }
    ctx.fillStyle = "#3a2f5b"; ctx.font = "14px sans-serif";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(nt.freq > 0 ? nt.note : "·", x, H * 0.93);
  });
}

// ===========================================================================
// 🤖 MAZE renderer — walk the robot through the maze and check the goal.
// ===========================================================================
function mazeRender(commands, maze) {
  if (!maze) { statusEl.textContent = "(no maze)"; return; }
  const rows = maze.rows, R = rows.length, C = rows[0].length;
  const order = ["up", "right", "down", "left"];
  const dv = { up: [-1, 0], right: [0, 1], down: [1, 0], left: [0, -1] };
  let r = maze.start[0], c = maze.start[1], d = maze.facing, bonk = false;
  const states = [{ r, c, d }];
  for (const cmd of commands) {
    if (bonk) break;
    if (cmd === "left") d = order[(order.indexOf(d) + 3) % 4];
    else if (cmd === "right") d = order[(order.indexOf(d) + 1) % 4];
    else {
      const nr = r + dv[d][0], nc = c + dv[d][1];
      if (nr < 0 || nr >= R || nc < 0 || nc >= C || rows[nr][nc] === "#") { bonk = true; states.push({ r, c, d, bonk: true }); continue; }
      r = nr; c = nc;
    }
    states.push({ r, c, d });
  }
  const reached = !bonk && r === maze.goal[0] && c === maze.goal[1];
  let i = 0;
  function step() {
    drawMaze(maze, states[i]);
    setProgress((i + 1) / states.length);
    if (i >= states.length - 1) {
      if (reached) cheer("🎉 You solved it!", { chime: true });
      else if (bonk) statusEl.textContent = "🤖 Bonk! That hit a wall — try different moves.";
      else statusEl.textContent = "🤖 Not at the star yet — keep trying!";
      return;
    }
    i++;
    mazeTimer = setTimeout(step, 350);
  }
  statusEl.textContent = "🤖 Going...";
  step();
}
function drawMaze(maze, s) {
  const rows = maze.rows, R = rows.length, C = rows[0].length;
  ctx.clearRect(0, 0, W, H);
  const pad = 24;
  const cs = Math.floor(Math.min((W - 2 * pad) / C, (H - 2 * pad) / R));
  const ox = (W - cs * C) / 2, oy = (H - cs * R) / 2;
  for (let rr = 0; rr < R; rr++) {
    for (let cc = 0; cc < C; cc++) {
      ctx.fillStyle = rows[rr][cc] === "#" ? "#5b4b8a" : "#ffffff";
      ctx.fillRect(ox + cc * cs + 1, oy + rr * cs + 1, cs - 2, cs - 2);
    }
  }
  ctx.font = Math.floor(cs * 0.62) + "px serif";
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillText("⭐", ox + maze.goal[1] * cs + cs / 2, oy + maze.goal[0] * cs + cs / 2);
  ctx.fillText("🤖", ox + s.c * cs + cs / 2, oy + s.r * cs + cs / 2);
}

// ===========================================================================
// 🏃 MOVE renderer — play the recorded frames as an animation.
// ===========================================================================
function animRender(frames) {
  if (!frames.length) { statusEl.textContent = "(nothing to move)"; return; }
  const per = Math.max(28, Math.min(120, 1600 / frames.length));
  let start = null;
  function frame(now) {
    if (start === null) start = now;
    const idx = Math.min(frames.length - 1, Math.floor((now - start) / per));
    drawScene(frames[idx]);
    setProgress((idx + 1) / frames.length);
    if (idx >= frames.length - 1) {
      cheer("🎉 You did it!"); animId = null; return;
    }
    animId = requestAnimationFrame(frame);
  }
  statusEl.textContent = "Playing... 🏃";
  animId = requestAnimationFrame(frame);
}
function drawScene(scene) {
  ctx.clearRect(0, 0, W, H);
  for (const sp of scene) {
    ctx.font = Math.floor(sp.size) + "px serif";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(sp.emoji, W / 2 + sp.x, H / 2 - sp.y);
  }
}

// ===========================================================================
// 🕹️ PLAY renderer — show the scene and react to keys / clicks.
// ===========================================================================
function interactiveRender(result) {
  currentSid = result.sid;
  drawScene(result.scene);
  setProgress(0);
  dpadEl.hidden = !result.handlers.key;   // show the on-screen arrows for tablets
  const how = [];
  if (result.handlers.key) how.push("the ARROW KEYS or buttons");
  if (result.handlers.click) how.push("CLICK the picture");
  statusEl.textContent = how.length ? ("🎮 Click here, then use " + how.join(" and ") + "!") : "🎮 Ready!";

  if (result.handlers.key) {
    interactiveKey = (e) => {
      const map = { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up", ArrowDown: "down",
                    a: "left", d: "right", w: "up", s: "down" };
      const k = map[e.key];
      if (!k) return;
      e.preventDefault();
      sendEvent({ type: "key", key: k });
    };
    canvas.addEventListener("keydown", interactiveKey);
  }
  if (result.handlers.click) {
    interactiveClick = (e) => {
      const rect = canvas.getBoundingClientRect();
      const sx = (e.clientX - rect.left) * (W / rect.width);
      const sy = (e.clientY - rect.top) * (H / rect.height);
      sendEvent({ type: "click", x: sx - W / 2, y: H / 2 - sy });
    };
    canvas.addEventListener("click", interactiveClick);
  }
  canvas.focus();
}
function sendEvent(ev) {
  if (!currentSid) return;
  ev.sid = currentSid;
  fetch("/event", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(ev),
  })
    .then(r => r.json())
    .then(res => {
      if (res.error) {
        consoleEl.textContent = "Oops: " + res.error.type + ": " + res.error.message;
        consoleEl.className = "error";
      }
      drawScene(res.scene || []);
    })
    .catch(() => {});
}
