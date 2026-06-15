"""
kidturtle  -  a tiny, kid-friendly drawing helper.

Your child writes simple commands like:

    from kidturtle import Turtle
    t = Turtle()
    t.forward(100)
    t.right(90)
    t.forward(100)
    t.show()

...and a colorful picture DRAWS ITSELF in the web browser.

Why this instead of Python's built-in `turtle`?
  * Python's `turtle` needs an extra piece called "tkinter" that is not
    installed on every Mac. This helper needs nothing extra at all.
  * Watching the line draw in the browser is the same magic that makes
    turtle drawing so good for learning "one step at a time" thinking.

Parents: you do not need to understand this file. The kids' scripts in the
numbered folders are the ones to read and change together. This is just the
"engine" that turns their commands into a picture.
"""

import json
import math
import os
import tempfile
import time
import webbrowser


class Turtle:
    """A pretend turtle that holds a pen and walks around, drawing as it goes."""

    def __init__(self, color="blue", width=4, background="#fdf6ff"):
        # Where the turtle is. (0, 0) is the middle of the picture.
        self.x = 0.0
        self.y = 0.0
        # Which way the turtle is facing, in degrees. 0 = to the right (east).
        self.heading = 0.0
        # Is the pen touching the paper? If yes, moving draws a line.
        self.pen_down = True
        self.pen_color = color
        self.pen_width = width
        self.background = background
        # Every line and dot we make gets remembered here so we can
        # play the whole drawing back, step by step, in the browser.
        self._ops = []

    # ---- moving around -------------------------------------------------

    def forward(self, distance):
        """Walk forward by `distance` steps (drawing a line if the pen is down)."""
        radians = math.radians(self.heading)
        new_x = self.x + distance * math.cos(radians)
        new_y = self.y + distance * math.sin(radians)
        self._move_to(new_x, new_y)

    def backward(self, distance):
        """Walk backward by `distance` steps."""
        self.forward(-distance)

    def right(self, angle):
        """Turn to the right (clockwise) by `angle` degrees."""
        self.heading -= angle

    def left(self, angle):
        """Turn to the left (counter-clockwise) by `angle` degrees."""
        self.heading += angle

    def goto(self, x, y):
        """Jump straight to a spot. (0, 0) is the middle."""
        self._move_to(float(x), float(y))

    def home(self):
        """Go back to the middle and face right again."""
        self.penup()
        self.goto(0, 0)
        self.heading = 0.0
        self.pendown()

    # ---- the pen -------------------------------------------------------

    def penup(self):
        """Lift the pen up. Now moving does NOT draw."""
        self.pen_down = False

    def pendown(self):
        """Put the pen down. Now moving DOES draw."""
        self.pen_down = True

    def color(self, name):
        """Change the pen color, like 'red', 'gold', 'hotpink', 'skyblue'."""
        self.pen_color = name

    def width(self, size):
        """Make the line thinner or thicker."""
        self.pen_width = size

    def dot(self, size=12, color=None):
        """Stamp a round dot right where the turtle is standing."""
        self._ops.append({
            "type": "dot",
            "x": self.x,
            "y": self.y,
            "r": size / 2.0,
            "color": color if color else self.pen_color,
        })

    def circle(self, radius, steps=60):
        """Draw a circle by taking lots of tiny steps and small turns."""
        # A circle is just a many-sided shape with very short sides.
        step_length = (2 * math.pi * radius) / steps
        turn = 360.0 / steps
        for _ in range(steps):
            self.forward(step_length)
            self.left(turn)

    # ---- show the picture ---------------------------------------------

    def show(self, title="My Drawing"):
        """Open the web browser and watch the whole picture draw itself!"""
        html = _build_html(self._ops, self.background, title)
        # Save the picture to a temporary file and open it in the browser.
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", prefix="kidturtle_", delete=False, encoding="utf-8"
        )
        handle.write(html)
        handle.close()
        print("Opening your drawing in the web browser... 🎨")
        print("(If it does not pop up, open this file:)")
        print("   " + handle.name)
        webbrowser.open("file://" + os.path.abspath(handle.name))
        # Give the browser a moment to grab the file before the script ends.
        time.sleep(1.0)

    # ---- short nicknames kids/parents might try -----------------------
    fd = forward
    bk = back = backward
    rt = right
    lt = left
    pencolor = color
    pensize = width

    # ---- the part that records each move ------------------------------

    def _move_to(self, new_x, new_y):
        if self.pen_down:
            self._ops.append({
                "type": "line",
                "x1": self.x,
                "y1": self.y,
                "x2": new_x,
                "y2": new_y,
                "color": self.pen_color,
                "width": self.pen_width,
            })
        else:
            self._ops.append({
                "type": "move",
                "x1": self.x,
                "y1": self.y,
                "x2": new_x,
                "y2": new_y,
            })
        self.x = new_x
        self.y = new_y


def _build_html(ops, background, title):
    """Turn the list of moves into a web page that animates the drawing."""
    ops_json = json.dumps(ops)
    safe_title = title.replace("<", "").replace(">", "")
    # The page draws each step one-by-one so kids see the order of instructions.
    return _TEMPLATE.replace("__TITLE__", safe_title) \
                    .replace("__BG__", background) \
                    .replace("__OPS__", ops_json)


_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  html, body {
    margin: 0; padding: 0; height: 100%;
    font-family: "Comic Sans MS", "Chalkboard SE", "Trebuchet MS", sans-serif;
    background: linear-gradient(160deg, #fef9ff, #eef6ff);
    color: #4a3f6b;
    text-align: center;
  }
  h1 { font-size: 2.2rem; margin: 18px 0 6px; }
  p.sub { margin: 0 0 14px; font-size: 1.1rem; color: #7a6f9b; }
  #stage {
    background: __BG__;
    border: 8px solid #b692f6;
    border-radius: 24px;
    box-shadow: 0 12px 30px rgba(120, 90, 200, .25);
    display: block;
    margin: 0 auto;
    max-width: 92vw;
    height: auto;
  }
  button {
    font: inherit; font-size: 1.3rem;
    margin: 18px 8px; padding: 12px 26px;
    border: none; border-radius: 999px; cursor: pointer;
    background: #ffb703; color: #5a3d00;
    box-shadow: 0 5px 0 #d99400;
    transition: transform .05s ease;
  }
  button:active { transform: translateY(3px); box-shadow: 0 2px 0 #d99400; }
  #done { font-size: 1.6rem; height: 2rem; margin-top: 8px; color: #2a9d8f; }
</style>
</head>
<body>
  <h1>🐢 __TITLE__</h1>
  <p class="sub">Watch the turtle draw, one step at a time!</p>
  <canvas id="stage" width="720" height="560"></canvas>
  <div id="done">&nbsp;</div>
  <div>
    <button onclick="play()">▶ Play again</button>
  </div>

<script>
const OPS = __OPS__;
const canvas = document.getElementById("stage");
const ctx = canvas.getContext("2d");
const doneText = document.getElementById("done");

// Work out a transform so the whole drawing fits nicely on the canvas,
// no matter how big or small the numbers the child chose were.
function computeFit() {
  let minX = 0, maxX = 0, minY = 0, maxY = 0, found = false;
  for (const op of OPS) {
    const pts = (op.type === "dot")
      ? [[op.x, op.y]]
      : [[op.x1, op.y1], [op.x2, op.y2]];
    for (const [px, py] of pts) {
      if (!found) { minX = maxX = px; minY = maxY = py; found = true; }
      minX = Math.min(minX, px); maxX = Math.max(maxX, px);
      minY = Math.min(minY, py); maxY = Math.max(maxY, py);
    }
  }
  if (!found) { minX = maxX = minY = maxY = 0; }
  const pad = 50;
  const drawW = (maxX - minX) || 1;
  const drawH = (maxY - minY) || 1;
  let scale = Math.min((canvas.width - 2 * pad) / drawW,
                       (canvas.height - 2 * pad) / drawH);
  if (!isFinite(scale) || scale <= 0) scale = 1;
  scale = Math.min(scale, 3);  // don't blow tiny drawings up too much
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;
  return { scale, cx, cy };
}
const fit = computeFit();

// Turn turtle coordinates (middle = 0,0, up = positive) into canvas pixels
// (top-left = 0,0, down = positive).
function tx(x) { return canvas.width / 2 + (x - fit.cx) * fit.scale; }
function ty(y) { return canvas.height / 2 - (y - fit.cy) * fit.scale; }

function drawTurtle(x, y) {
  ctx.save();
  ctx.font = "26px serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("🐢", x, y);
  ctx.restore();
}

let animId = null;

function play() {
  if (animId) cancelAnimationFrame(animId);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  doneText.innerHTML = "&nbsp;";

  // How fast to draw: lots of steps -> go quick; few steps -> slow & clear.
  const drawn = OPS.filter(o => o.type === "line").length || 1;
  const perStep = Math.max(12, Math.min(260, 4200 / drawn)); // milliseconds

  let i = 0;
  let stepStart = null;

  function frame(now) {
    if (stepStart === null) stepStart = now;
    if (i >= OPS.length) {
      // All finished. Stamp the turtle at the very last spot.
      const last = OPS[OPS.length - 1];
      if (last) {
        const ex = last.type === "dot" ? last.x : last.x2;
        const ey = last.type === "dot" ? last.y : last.y2;
        drawTurtle(tx(ex), ty(ey));
      }
      doneText.textContent = "🎉 You did it!";
      animId = null;
      return;
    }

    const op = OPS[i];

    if (op.type === "dot") {
      ctx.beginPath();
      ctx.fillStyle = op.color;
      ctx.arc(tx(op.x), ty(op.y), Math.max(2, op.r * fit.scale), 0, Math.PI * 2);
      ctx.fill();
      i++; stepStart = now;
      animId = requestAnimationFrame(frame);
      return;
    }

    // A line or a pen-up move: animate from start point to end point.
    const t = Math.min(1, (now - stepStart) / perStep);
    const curX = op.x1 + (op.x2 - op.x1) * t;
    const curY = op.y1 + (op.y2 - op.y1) * t;

    // Redraw everything finished so far (kept simple and reliable).
    redrawCommitted(i);

    if (op.type === "line") {
      ctx.beginPath();
      ctx.strokeStyle = op.color;
      ctx.lineWidth = Math.max(1, op.width * fit.scale);
      ctx.lineCap = "round";
      ctx.moveTo(tx(op.x1), ty(op.y1));
      ctx.lineTo(tx(curX), ty(curY));
      ctx.stroke();
    }
    drawTurtle(tx(curX), ty(curY));

    if (t >= 1) { i++; stepStart = now; }
    animId = requestAnimationFrame(frame);
  }

  animId = requestAnimationFrame(frame);
}

// Draw every completed step up to (but not including) index `upto`.
function redrawCommitted(upto) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let k = 0; k < upto; k++) {
    const op = OPS[k];
    if (op.type === "line") {
      ctx.beginPath();
      ctx.strokeStyle = op.color;
      ctx.lineWidth = Math.max(1, op.width * fit.scale);
      ctx.lineCap = "round";
      ctx.moveTo(tx(op.x1), ty(op.y1));
      ctx.lineTo(tx(op.x2), ty(op.y2));
      ctx.stroke();
    } else if (op.type === "dot") {
      ctx.beginPath();
      ctx.fillStyle = op.color;
      ctx.arc(tx(op.x), ty(op.y), Math.max(2, op.r * fit.scale), 0, Math.PI * 2);
      ctx.fill();
    }
  }
}

play();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    # A little demo so you can test that everything works:
    #     python3 kidturtle.py
    demo = Turtle()
    for color in ["red", "orange", "gold", "green", "blue", "purple"]:
        demo.color(color)
        demo.forward(120)
        demo.right(60)
    demo.show("Hello from kidturtle!")
