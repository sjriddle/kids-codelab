"""
The Code Lab! 🧪  (multi-track lesson hub)

Run this with:
    python3 08_code_lab/code_lab.py

Everything happens in your web browser: pick a lesson, read the goal, wiggle the
knobs or edit the code, and press ▶ Run. The Lab has several TRACKS:

  🎨 Draw   – turtle drawing (sequence, loops, variables, lists)
  🎵 Music  – write code that plays tunes
  🤖 Maze   – steer a robot to the goal (algorithms & debugging)
  🏃 Move   – simple animations (things change over time)
  🕹️ Play   – interactive programs that react to keys & clicks

No installing anything. No text editor needed.
When you're done, come back to the Terminal and press Ctrl + C.

----------------------------------------------------------------------
For grown-ups: this server runs the Python your child writes, on YOUR
computer only (locked to 127.0.0.1). It's for local learning, the same
as running `python3 some_file.py` yourself.
----------------------------------------------------------------------
"""

import contextlib
import functools
import http.server
import io
import json
import math
import os
import random
import socketserver
import sys
import threading
import traceback
import webbrowser

# Find our drawing helper (kidturtle.py ) in the folder above this one.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kidturtle  # noqa: E402

WEB_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
RUN_LOCK = threading.Lock()

# Safety caps so a runaway loop can't freeze the page.
MAX_OPS = 30000
MAX_NOTES = 2000
MAX_COMMANDS = 5000
MAX_FRAMES = 4000
MAX_SPRITES = 60

# While a program runs, the objects it creates register themselves here.
_collect = None


def _register(kind, obj):
    if _collect is not None:
        _collect[kind].append(obj)


# --------------------------------------------------------------------------
# 🎨 DRAW: a turtle that records its drawing instead of opening a new tab.
# --------------------------------------------------------------------------
class LabTurtle(kidturtle.Turtle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._title = "My Drawing"
        _register("turtles", self)

    def show(self, title="My Drawing"):
        self._title = title

    def _move_to(self, x, y):
        super()._move_to(x, y)
        if len(self._ops) > MAX_OPS:
            raise RuntimeError("Whoa! That's a LOT of drawing. Try smaller numbers. 🐢")

    def dot(self, size=12, color=None):
        super().dot(size, color)
        if len(self._ops) > MAX_OPS:
            raise RuntimeError("Whoa! That's a LOT of drawing. Try smaller numbers. 🐢")


# --------------------------------------------------------------------------
# 🎵 MUSIC: a song that records notes for the browser to play.
# --------------------------------------------------------------------------
_LETTERS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note_to_freq(name):
    """Turn a note name like 'C', 'C4', 'F#5', 'Bb3' into a frequency in Hz."""
    name = str(name).strip()
    if name == "" or name.lower() in ("rest", "r"):
        return 0.0
    letter = name[0].upper()
    if letter not in _LETTERS:
        return 0.0
    semis = _LETTERS[letter]
    i = 1
    if i < len(name) and name[i] in "#b":
        semis += 1 if name[i] == "#" else -1
        i += 1
    octave = int(name[i:]) if name[i:].lstrip("-").isdigit() else 4
    midi = semis + (octave + 1) * 12          # C4 = MIDI 60
    return round(440.0 * (2 ** ((midi - 69) / 12.0)), 2)


class Song:
    def __init__(self, tempo=120):
        self.bpm = tempo
        self.notes = []
        _register("songs", self)

    def tempo(self, bpm):
        self.bpm = bpm

    def play(self, note, beats=1):
        self.notes.append({"note": str(note), "freq": note_to_freq(note), "beats": float(beats)})
        self._guard()

    def rest(self, beats=1):
        self.notes.append({"note": "rest", "freq": 0.0, "beats": float(beats)})
        self._guard()

    def _guard(self):
        if len(self.notes) > MAX_NOTES:
            raise RuntimeError("Whoa! That's a LOT of notes. Try a shorter song. 🎵")


# --------------------------------------------------------------------------
# 🤖 MAZE: a robot that records its moves; the browser walks the maze.
# --------------------------------------------------------------------------
class Robot:
    def __init__(self):
        self.commands = []
        _register("robots", self)

    def forward(self, steps=1):
        for _ in range(int(steps)):
            self.commands.append("forward")
            self._guard()

    def left(self):
        self.commands.append("left")
        self._guard()

    def right(self):
        self.commands.append("right")
        self._guard()

    def _guard(self):
        if len(self.commands) > MAX_COMMANDS:
            raise RuntimeError("Whoa! That's a LOT of moves. Try fewer steps. 🤖")


# --------------------------------------------------------------------------
# 🏃 MOVE / 🕹️ PLAY: a stage with emoji sprites you can move around.
# --------------------------------------------------------------------------
class Sprite:
    def __init__(self, stage, emoji, x, y, size):
        self.stage = stage
        self.emoji = emoji
        self.x = float(x)
        self.y = float(y)
        self.size = float(size)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.stage._frame()

    def go_to(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.stage._frame()

    def grow(self, amount):
        self.size = max(6, self.size + amount)
        self.stage._frame()


class Stage:
    def __init__(self, background="#eaf6ff"):
        self.sprites = []
        self.frames = []
        self.background = background
        _register("stages", self)

    def add(self, emoji, x=0, y=0, size=44):
        if len(self.sprites) >= MAX_SPRITES:
            raise RuntimeError("That's a lot of characters! Try fewer. 🏃")
        s = Sprite(self, emoji, x, y, size)
        self.sprites.append(s)
        self._frame()
        return s

    def snapshot(self):
        self._frame()

    def current(self):
        return [{"emoji": s.emoji, "x": s.x, "y": s.y, "size": s.size} for s in self.sprites]

    def _frame(self):
        self.frames.append(self.current())
        if len(self.frames) > MAX_FRAMES:
            self.frames.pop(0)


# --------------------------------------------------------------------------
# Running code & deciding what kind of result it produced.
# --------------------------------------------------------------------------
SESSIONS = {}            # interactive sessions: id -> {ns, stage}
_session_counter = 0


def _new_namespace():
    return {
        "Turtle": LabTurtle, "Song": Song, "Robot": Robot, "Stage": Stage,
        "random": random, "math": math,
    }


def _describe_error(e, code_name="<your code>"):
    if isinstance(e, SyntaxError):
        return {"type": "SyntaxError", "message": e.msg, "line": e.lineno}
    line = None
    for frame in traceback.extract_tb(e.__traceback__):
        if frame.filename == code_name:
            line = frame.lineno
    return {"type": type(e).__name__, "message": str(e), "line": line}


def run_code(code):
    global _collect, _session_counter
    coll = {"turtles": [], "songs": [], "robots": [], "stages": []}
    ns = _new_namespace()
    out = io.StringIO()
    error = None
    _collect = coll
    try:
        compiled = compile(code, "<your code>", "exec")
        with contextlib.redirect_stdout(out):
            exec(compiled, ns)              # noqa: S102 (local, trusted, on purpose)
    except Exception as e:                  # noqa: BLE001
        error = _describe_error(e)
    finally:
        _collect = None

    base = {"ok": error is None, "output": out.getvalue(), "error": error}

    if coll["stages"]:
        stage = coll["stages"][-1]
        if callable(ns.get("on_key")) or callable(ns.get("on_click")):
            _session_counter += 1
            sid = "s" + str(_session_counter)
            SESSIONS[sid] = {"ns": ns, "stage": stage}
            while len(SESSIONS) > 20:
                SESSIONS.pop(next(iter(SESSIONS)))
            base.update({
                "kind": "interactive", "sid": sid, "scene": stage.current(),
                "background": stage.background,
                "handlers": {"key": callable(ns.get("on_key")),
                             "click": callable(ns.get("on_click"))},
            })
        else:
            base.update({"kind": "anim", "frames": stage.frames or [stage.current()],
                         "background": stage.background})
    elif coll["robots"]:
        base.update({"kind": "maze", "commands": coll["robots"][-1].commands})
    elif coll["songs"]:
        song = coll["songs"][-1]
        base.update({"kind": "music", "notes": song.notes, "bpm": song.bpm})
    else:
        ops, bg, title = [], "#fdf6ff", "My Drawing"
        for t in coll["turtles"]:
            ops.extend(t._ops)
            bg, title = t.background, t._title
        base.update({"kind": "draw", "ops": ops, "background": bg, "title": title})

    return base


def run_event(sid, ev_type, key=None, x=None, y=None):
    """Handle a key/click for an interactive program, then return the new scene."""
    sess = SESSIONS.get(sid)
    if not sess:
        return {"ok": False, "scene": [], "error": {"type": "Gone",
                "message": "Press Run again to start playing.", "line": None}, "output": ""}
    ns, stage = sess["ns"], sess["stage"]
    out = io.StringIO()
    error = None
    try:
        with contextlib.redirect_stdout(out):
            if ev_type == "key" and callable(ns.get("on_key")):
                ns["on_key"](key)
            elif ev_type == "click" and callable(ns.get("on_click")):
                ns["on_click"](x, y)
    except Exception as e:                  # noqa: BLE001
        error = _describe_error(e)
    return {"ok": error is None, "scene": stage.current(), "error": error, "output": out.getvalue()}


# --------------------------------------------------------------------------
# The lessons, grouped into tracks.
# --------------------------------------------------------------------------
def _maze(rows, start, facing, goal):
    return {"rows": rows, "start": start, "facing": facing, "goal": goal}


LESSONS = [
    # ---------------- 🎨 DRAW ----------------
    {"track": "🎨 Draw", "title": "A square", "emoji": "⬛",
     "goal": "Make a square. Then make it BIGGER by changing the size.",
     "tip": "Unplugged first: walk a square together — forward, turn, four times. "
            "A loop just says 'do it 4 times'.",
     "code": 'color = "green"\nsize = 150\n\nt = Turtle()\nt.color(color)\nt.width(6)\n\nfor side in range(4):\n    t.forward(size)\n    t.right(90)\n\nt.show()\n'},
    {"track": "🎨 Draw", "title": "Any shape", "emoji": "🔺",
     "goal": "Change 'sides' to draw a triangle (3), a pentagon (5), a hexagon (6)!",
     "tip": "The turn is always 360 ÷ number of sides. Try big numbers — it becomes a circle!",
     "code": 'color = "red"\nsides = 5\nsize = 160\n\nt = Turtle()\nt.color(color)\nt.width(6)\nturn = 360 / sides\n\nfor side in range(sides):\n    t.forward(size)\n    t.right(turn)\n\nt.show()\n'},
    {"track": "🎨 Draw", "title": "A flower", "emoji": "🌸",
     "goal": "Give your flower more petals. Try a new color!",
     "tip": "Each petal is a circle, turned a little. More petals = smaller turn.",
     "code": 'color = "deeppink"\npetals = 9\nsize = 70\n\nt = Turtle()\nt.color(color)\nt.width(2)\nturn = 360 / petals\n\nfor petal in range(petals):\n    t.circle(size)\n    t.right(turn)\n\nt.dot(40, "gold")\nt.show()\n'},
    {"track": "🎨 Draw", "title": "Spinning squares", "emoji": "🌀",
     "goal": "A loop inside a loop! Change 'squares' and watch the pattern spin.",
     "tip": "The inside loop draws one square; the outside loop turns a little and does it again.",
     "code": 'color = "magenta"\nsquares = 12\nsize = 140\n\nt = Turtle()\nt.color(color)\nt.width(2)\nturn = 360 / squares\n\nfor s in range(squares):\n    for side in range(4):\n        t.forward(size)\n        t.right(90)\n    t.right(turn)\n\nt.show()\n'},
    {"track": "🎨 Draw", "title": "Rainbow spiral", "emoji": "🌈",
     "goal": "Watch it spiral out in rainbow colors! Try changing 'steps' or 'angle'.",
     "tip": "A LIST of colors is used one at a time, and each line grows a little longer.",
     "code": 'steps = 60\nangle = 59\ngrow = 4\n\nt = Turtle()\nt.width(4)\nrainbow = ["red", "orange", "gold", "green", "blue", "purple"]\nlength = 5\n\nfor step in range(steps):\n    t.color(rainbow[step % len(rainbow)])\n    t.forward(length)\n    t.right(angle)\n    length = length + grow\n\nt.show()\n'},
    {"track": "🎨 Draw", "title": "Rainbow star", "emoji": "⭐",
     "goal": "A five-point star, each point a different color. Make it bigger!",
     "tip": "The magic star angle is 144. Each point uses the next color in the list.",
     "code": 'size = 250\n\nt = Turtle()\nt.width(5)\nstar_colors = ["red", "gold", "limegreen", "deepskyblue", "violet"]\n\nfor point in range(5):\n    t.color(star_colors[point])\n    t.forward(size)\n    t.right(144)\n\nt.show()\n'},
    {"track": "🎨 Draw", "title": "Polka dots", "emoji": "🔴",
     "goal": "Surprise dots everywhere! Run it again — it's different every time.",
     "tip": "random puts each dot in a surprise spot, size, and color. Change 'how_many'.",
     "code": 'how_many = 25\n\nt = Turtle()\ncolors = ["red", "orange", "gold", "green", "blue", "purple", "hotpink", "cyan"]\n\nfor dot in range(how_many):\n    t.penup()\n    t.goto(random.randint(-250, 250), random.randint(-200, 200))\n    t.dot(random.randint(20, 60), random.choice(colors))\n\nt.show()\n'},

    {"track": "🎨 Draw", "title": "Free draw", "emoji": "🎪",
     "goal": "No rules — make ANYTHING! Use the command menu in the code.",
     "tip": "Pure play, no goal. Let your child invent and describe what they make. "
            "Read the command menu together and pick commands to try.",
     "code": '# 🎨 Free draw! Mix and match the commands below.\ncolor = "purple"\n\nt = Turtle()\nt.color(color)\nt.width(8)\n\n# ---- Commands you can use ----\n#   t.color("red")      change color\n#   t.width(10)         line thickness\n#   t.forward(100)      go forward\n#   t.backward(100)     go back\n#   t.left(90)          turn left\n#   t.right(90)         turn right\n#   t.circle(60)        draw a circle\n#   t.dot(30, "gold")   stamp a dot\n#   t.penup()           move without drawing\n#   t.pendown()         draw again\n# ------------------------------\n\nt.forward(120)\nt.left(120)\nt.forward(120)\nt.dot(40, "gold")\n\nt.show()\n'},

    # ---------------- 🎵 Music ----------------
    {"track": "🎵 Music", "title": "First notes", "emoji": "🎵",
     "goal": "Press Run to hear the notes. Change a note letter (A–G) and listen!",
     "tip": "Notes go from A to G. Add a number for higher/lower, like C5. This is a "
            "SEQUENCE you can hear — order matters!",
     "code": 'song = Song()\n\nsong.play("C", 1)\nsong.play("E", 1)\nsong.play("G", 1)\nsong.play("C5", 2)\n'},
    {"track": "🎵 Music", "title": "A loop tune", "emoji": "🔁",
     "goal": "Change 'times' to repeat the little tune more. Change 'speed' to go faster!",
     "tip": "Same loop idea as drawing — but now you hear the repeats.",
     "code": 'times = 4\nspeed = 140\n\nsong = Song(speed)\nfor i in range(times):\n    song.play("C", 1)\n    song.play("G", 1)\n    song.play("E", 1)\n    song.rest(1)\n'},
    {"track": "🎵 Music", "title": "Twinkle Twinkle", "emoji": "⭐",
     "goal": "It's a real song from a LIST of notes! Try changing 'speed', or some notes.",
     "tip": "A list holds the whole melody. The loop plays each note in order.",
     "code": 'speed = 120\n\nsong = Song(speed)\nmelody = ["C","C","G","G","A","A","G",\n          "F","F","E","E","D","D","C"]\n\nfor note in melody:\n    song.play(note, 1)\n'},

    {"track": "🎵 Music", "title": "Free music", "emoji": "🎪",
     "goal": "Make your own tune! Add, change, or remove notes.",
     "tip": "A blank stage for melodies. Try a song you know, or a silly one. "
            "Numbers after a note (like C5) change how high it sounds.",
     "code": '# 🎵 Free play! Add your own notes.\nspeed = 130\n\nsong = Song(speed)\n\n# ---- Commands you can use ----\n#   song.play("C", 1)   play a note (A B C D E F G)\n#   song.play("C5", 2)  a number = higher/lower; 2 = longer\n#   song.rest(1)        a quiet beat\n# ------------------------------\n\nsong.play("C", 1)\nsong.play("E", 1)\nsong.play("G", 1)\nsong.rest(1)\nsong.play("G", 1)\nsong.play("E", 1)\nsong.play("C", 2)\n'},

    # ---------------- 🤖 Maze ----------------
    {"track": "🤖 Maze", "title": "Straight to the star", "emoji": "➡️",
     "goal": "Steer the robot to the ⭐. How many steps forward does it need?",
     "tip": "Count the cells out loud together. This is debugging: too few or too many "
            "steps and you miss the star — fix the number!",
     "code": 'robot = Robot()\n\nrobot.forward(2)\n',
     "maze": _maze(["#######", "#.....#", "#######"], [1, 1], "right", [1, 5])},
    {"track": "🤖 Maze", "title": "Around the corner", "emoji": "↪️",
     "goal": "Go forward, then TURN, then forward again to reach the ⭐.",
     "tip": "robot.right() turns the robot (it doesn't move). Then forward to go the new way.",
     "code": 'robot = Robot()\n\nrobot.forward(2)\nrobot.right()\nrobot.forward(2)\n',
     "maze": _maze(["#####", "#...#", "###.#", "###.#", "#####"], [1, 1], "right", [3, 3])},
    {"track": "🤖 Maze", "title": "Turn left this time", "emoji": "↩️",
     "goal": "This time you must turn LEFT! Fix the turn so the robot reaches the ⭐.",
     "tip": "robot.left() turns the opposite way from robot.right(). Swap it and see.",
     "code": 'robot = Robot()\n\nrobot.forward(2)\nrobot.right()\nrobot.forward(2)\n',
     "maze": _maze(["#####", "###.#", "###.#", "#...#", "#####"], [3, 1], "right", [1, 3])},
    {"track": "🤖 Maze", "title": "The zig-zag", "emoji": "🔀",
     "goal": "A zig-zag! Forward, turn, forward, then turn again to reach the ⭐.",
     "tip": "Do it in parts: go to the first bend, turn, go to the next bend, turn, then forward to the star.",
     "code": 'robot = Robot()\n\nrobot.forward(2)\nrobot.right()\nrobot.forward(2)\n',
     "maze": _maze(["######", "#...##", "###.##", "###..#", "######"], [1, 1], "right", [3, 4])},
    {"track": "🤖 Maze", "title": "Don't overshoot", "emoji": "🎯",
     "goal": "Don't go too far! Turn down at exactly the right spot to reach the ⭐.",
     "tip": "Count the cells to the turn. Too many forwards and the robot bonks the wall.",
     "code": 'robot = Robot()\n\nrobot.forward(3)\nrobot.right()\nrobot.forward(2)\n',
     "maze": _maze(["######", "#....#", "###.##", "###.##", "######"], [1, 1], "right", [3, 3])},
    {"track": "🤖 Maze", "title": "The long hallway", "emoji": "🔁",
     "goal": "It's a long way! Use a LOOP so you don't write forward() seven times.",
     "tip": "for i in range(7): robot.forward(1) — the loop repeats the step for you.",
     "code": 'robot = Robot()\n\nfor step in range(3):\n    robot.forward(1)\n',
     "maze": _maze(["##########", "#........#", "##########"], [1, 1], "right", [1, 8])},
    {"track": "🤖 Maze", "title": "Climb the staircase", "emoji": "🪜",
     "goal": "Climb the staircase to the ⭐! Each stair is the same — try a loop.",
     "tip": "Each stair is: forward, turn left, forward, turn right. Put that pattern in a loop and repeat it.",
     "code": 'robot = Robot()\n\nfor step in range(2):\n    robot.forward(1)\n    robot.left()\n    robot.forward(1)\n    robot.right()\n',
     "maze": _maze(["#######", "#####.#", "####..#", "###..##", "##..###", "#..####", "#######"], [5, 1], "right", [1, 5])},

    {"track": "🤖 Maze", "title": "Free roam", "emoji": "🎪",
     "goal": "Explore the room! Drive around and try to reach the ⭐ your own way.",
     "tip": "An open room for trial and error — turning and moving freely with no "
            "pressure. Celebrate the happy accidents.",
     "code": '# 🤖 Free roam! Drive the robot. Can you reach the star?\nrobot = Robot()\n\n# ---- Commands ----\n#   robot.forward(1)   move forward one cell\n#   robot.left()       turn left\n#   robot.right()      turn right\n# ------------------\n\nrobot.forward(2)\nrobot.right()\nrobot.forward(2)\n',
     "maze": _maze(["#########", "#.......#", "#.......#", "#...#...#", "#.......#", "#.......#", "#########"], [1, 1], "right", [5, 7])},

    # ---------------- 🏃 Move ----------------
    {"track": "🏃 Move", "title": "Fly the rocket", "emoji": "🚀",
     "goal": "Make the rocket fly across. Change 'steps' or 'speed' (how far each hop).",
     "tip": "Each move records a frame; the loop builds an animation. More steps = longer flight.",
     "code": 'steps = 24\nspeed = 18\n\nstage = Stage()\nrocket = stage.add("🚀", -220, 0)\n\nfor i in range(steps):\n    rocket.move(speed, 0)\n'},
    {"track": "🏃 Move", "title": "Bouncing ball", "emoji": "⚽",
     "goal": "The ball goes right, then comes back. Change the numbers to bounce farther!",
     "tip": "Two loops: one moving right, one moving left. That's a sequence of motions.",
     "code": 'hops = 18\n\nstage = Stage()\nball = stage.add("⚽", -180, 0)\n\nfor i in range(hops):\n    ball.move(20, 0)\nfor i in range(hops):\n    ball.move(-20, 0)\n'},
    {"track": "🏃 Move", "title": "A little scene", "emoji": "🐢",
     "goal": "Two characters moving! Make the turtle chase the rabbit, or add your own.",
     "tip": "You can move more than one sprite. Try giving them different speeds.",
     "code": 'steps = 20\n\nstage = Stage("#eafbe7")\nrabbit = stage.add("🐰", -200, 60)\nturtle = stage.add("🐢", -200, -60)\n\nfor i in range(steps):\n    rabbit.move(18, 0)\n    turtle.move(12, 0)\n'},

    {"track": "🏃 Move", "title": "Free moves", "emoji": "🎪",
     "goal": "Make your own moving scene! Change the emoji and the moves.",
     "tip": "Each move is one animation frame; a loop makes smooth motion. Let them "
            "add favorite emoji characters and different speeds.",
     "code": '# 🏃 Free play! Move your characters around.\nsteps = 20\n\nstage = Stage("#eaf6ff")\nhero = stage.add("🐱", -200, 0)\n\n# ---- Commands ----\n#   stage.add("🐶", 0, 0)    add a character (any emoji!)\n#   hero.move(10, 0)         move right (negative = left)\n#   hero.move(0, 10)         move up (negative = down)\n#   hero.go_to(0, 0)         jump to a spot\n#   hero.grow(10)            bigger (negative = smaller)\n# ------------------\n\nfor i in range(steps):\n    hero.move(20, 0)\n    hero.grow(2)\n'},

    # ---------------- 🕹️ Play ----------------
    {"track": "🕹️ Play", "title": "Drive the car", "emoji": "🚗",
     "goal": "Press Run, then click the picture and use the ARROW KEYS to drive! 🚗",
     "tip": "on_key runs every time a key is pressed. This is an EVENT — the program waits "
            "and reacts to you.",
     "code": 'stage = Stage("#eef")\ncar = stage.add("🚗", 0, 0)\n\ndef on_key(key):\n    if key == "right":\n        car.move(20, 0)\n    if key == "left":\n        car.move(-20, 0)\n    if key == "up":\n        car.move(0, 20)\n    if key == "down":\n        car.move(0, -20)\n'},
    {"track": "🕹️ Play", "title": "Magic star", "emoji": "⭐",
     "goal": "Press Run, then CLICK anywhere on the picture — the star jumps to you!",
     "tip": "on_click reacts to a mouse click and tells you where you clicked (x, y).",
     "code": 'stage = Stage("#fff7e6")\nstar = stage.add("⭐", 0, 0, 60)\n\ndef on_click(x, y):\n    star.go_to(x, y)\n'},

    {"track": "🕹️ Play", "title": "Free game", "emoji": "🎪",
     "goal": "Make your own game! Run it, click the picture, then play with the keys.",
     "tip": "Both keys AND clicks work here. Try making a key grow the hero, or clicks "
            "move it. Change the 🐱 to any character.",
     "code": '# 🕹️ Free play game! Run it, click the picture, then play.\nstage = Stage("#eef")\nhero = stage.add("🐱", 0, 0)\n\n# ---- React to keys and clicks ----\n#   def on_key(key):     runs on a key press\n#       key is "left" "right" "up" "down"\n#   def on_click(x, y):  runs when you click\n#   hero.move(dx, dy)  hero.go_to(x, y)  hero.grow(n)\n# ----------------------------------\n\ndef on_key(key):\n    if key == "right":\n        hero.move(20, 0)\n    if key == "left":\n        hero.move(-20, 0)\n    if key == "up":\n        hero.move(0, 20)\n    if key == "down":\n        hero.move(0, -20)\n\ndef on_click(x, y):\n    hero.grow(10)\n'},
]


# --------------------------------------------------------------------------
# The web server.
# --------------------------------------------------------------------------
class LabHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_FOLDER, **kwargs)

    def do_GET(self):
        if self.path == "/lessons":
            self._send_json(LESSONS)
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/run":
            data = self._read_json()
            with RUN_LOCK:
                result = run_code(data.get("code", ""))
            self._send_json(result)
        elif self.path == "/event":
            data = self._read_json()
            with RUN_LOCK:
                result = run_event(data.get("sid"), data.get("type"),
                                   data.get("key"), data.get("x"), data.get("y"))
            self._send_json(result)
        else:
            self.send_error(404)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return {}

    def _send_json(self, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def find_free_port(start=8050, tries=30):
    for port in range(start, start + tries):
        try:
            with socketserver.TCPServer(("127.0.0.1", port), http.server.BaseHTTPRequestHandler):
                return port
        except OSError:
            continue
    return start


def main():
    port = find_free_port()
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), LabHandler) as server:
        url = "http://localhost:" + str(port)
        print("=" * 54)
        print("  🧪  The Code Lab is OPEN!")
        print("  Opening your browser at: " + url)
        print("  Pick a lesson, then edit the code or wiggle the knobs.")
        print("  When you're done, press  Ctrl + C  here to stop.")
        print("=" * 54)
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Code Lab closed. See you next time!")


if __name__ == "__main__":
    main()
