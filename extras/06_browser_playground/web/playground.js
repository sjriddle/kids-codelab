// The brains of the drawing playground.
// (Parents: this is JavaScript, which runs in the browser. The kids' Python
//  lives in the other modules — this file just makes the web page interactive.)

const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

// ---- start with a clean white board ----
function clearBoard() {
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}
clearBoard();

// ---- what's currently selected ----
let color = "#e63946";   // the chosen pen color
let size = 30;           // the chosen brush size
let stamp = "";          // "" means "draw lines"; an emoji means "stamp it"
let rainbow = false;     // rainbow mode cycles colors as you draw
let hue = 0;             // used for the rainbow color

let drawing = false;
let lastX = 0, lastY = 0;

// ---- turn a mouse/touch position into a spot on the canvas ----
function getPos(event) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  return {
    x: (event.clientX - rect.left) * scaleX,
    y: (event.clientY - rect.top) * scaleY,
  };
}

function currentColor() {
  if (rainbow) {
    hue = (hue + 8) % 360;
    return "hsl(" + hue + ", 90%, 55%)";
  }
  return color;
}

function placeStamp(x, y) {
  ctx.font = (size * 2) + "px serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(stamp, x, y);
}

function paintLine(x, y) {
  ctx.strokeStyle = currentColor();
  ctx.lineWidth = size;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.beginPath();
  ctx.moveTo(lastX, lastY);
  ctx.lineTo(x, y);
  ctx.stroke();
  lastX = x;
  lastY = y;
}

// ---- pointer events work for both mouse and touchscreen ----
canvas.addEventListener("pointerdown", (e) => {
  const p = getPos(e);
  drawing = true;
  lastX = p.x;
  lastY = p.y;
  if (stamp) {
    placeStamp(p.x, p.y);
  } else {
    // a single click should leave a dot
    ctx.fillStyle = currentColor();
    ctx.beginPath();
    ctx.arc(p.x, p.y, size / 2, 0, Math.PI * 2);
    ctx.fill();
  }
});

canvas.addEventListener("pointermove", (e) => {
  if (!drawing) return;
  const p = getPos(e);
  if (stamp) {
    // only stamp every so often so we don't get a solid blob
    const dx = p.x - lastX, dy = p.y - lastY;
    if (Math.sqrt(dx * dx + dy * dy) > size * 1.5) {
      placeStamp(p.x, p.y);
      lastX = p.x;
      lastY = p.y;
    }
  } else {
    paintLine(p.x, p.y);
  }
});

window.addEventListener("pointerup", () => { drawing = false; });

// ---- color buttons ----
document.querySelectorAll(".swatch").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".swatch").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    if (btn.dataset.color === "rainbow") {
      rainbow = true;
    } else {
      rainbow = false;
      color = btn.dataset.color;
    }
  });
});

// ---- brush size buttons ----
document.querySelectorAll(".size").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".size").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    size = Number(btn.dataset.size);
  });
});

// ---- stamp buttons ----
document.querySelectorAll(".stamp").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".stamp").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    stamp = btn.dataset.stamp;   // "" for the Draw button
  });
});

// ---- clear and save ----
document.getElementById("clear").addEventListener("click", clearBoard);

document.getElementById("save").addEventListener("click", () => {
  const link = document.createElement("a");
  link.download = "my-drawing.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
});

// select sensible defaults on load
document.querySelector('.swatch[data-color="#e63946"]').classList.add("selected");
document.querySelector('.stamp[data-stamp=""]').classList.add("selected");
