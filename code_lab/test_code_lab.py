"""
Tests for the Code Lab engine.  Run with:

    python3 code_lab/test_code_lab.py

No extra libraries needed. Prints PASS/FAIL for each check and exits with a
non-zero code if anything fails, so it's easy to run after adding lessons.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import code_lab as L  # noqa: E402

_fails = 0


def check(name, cond):
    global _fails
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond:
        _fails += 1


def maze_solves(maze, commands):
    """Simulate the robot the same way the browser does, return True if it wins."""
    order = ["up", "right", "down", "left"]
    dv = {"up": (-1, 0), "right": (0, 1), "down": (1, 0), "left": (0, -1)}
    rows = maze["rows"]
    R, C = len(rows), len(rows[0])
    r, c, d = maze["start"][0], maze["start"][1], maze["facing"]
    bonk = False
    for cmd in commands:
        if bonk:
            break
        if cmd == "left":
            d = order[(order.index(d) + 3) % 4]
        elif cmd == "right":
            d = order[(order.index(d) + 1) % 4]
        else:
            nr, nc = r + dv[d][0], c + dv[d][1]
            if nr < 0 or nr >= R or nc < 0 or nc >= C or rows[nr][nc] == "#":
                bonk = True
                continue
            r, c = nr, nc
    return (not bonk) and r == maze["goal"][0] and c == maze["goal"][1]


def main():
    # ---- each track produces the right kind of result ----
    r = L.run_code('t = Turtle()\nfor i in range(4):\n    t.forward(120)\n    t.right(90)\nt.show()')
    check("draw -> 4 line ops", r["ok"] and r["kind"] == "draw" and len(r["ops"]) == 4)

    r = L.run_code('s = Song(120)\ns.play("C")\ns.play("G", 2)')
    check("music -> notes with frequencies", r["ok"] and r["kind"] == "music" and len(r["notes"]) == 2 and r["notes"][0]["freq"] > 0)

    r = L.run_code('robot = Robot()\nrobot.forward(2)\nrobot.right()')
    check("maze -> command list", r["ok"] and r["kind"] == "maze" and r["commands"] == ["forward", "forward", "right"])

    r = L.run_code('st = Stage()\nb = st.add("⚽", -50, 0)\nfor i in range(3):\n    b.move(10, 0)')
    check("anim -> recorded frames", r["ok"] and r["kind"] == "anim" and len(r["frames"]) == 4)

    r = L.run_code('st = Stage()\nc = st.add("🚗", 0, 0)\ndef on_key(key):\n    c.move(10, 0)')
    check("interactive -> session + handlers", r["ok"] and r["kind"] == "interactive" and r["handlers"]["key"])
    sid = r["sid"]
    e = L.run_event(sid, "key", key="right")
    e = L.run_event(sid, "key", key="right")
    check("interactive /event moves the sprite", e["scene"][0]["x"] == 20.0)
    check("stale session is handled kindly", not L.run_event("nope", "key", key="x")["ok"])

    # ---- music note maths ----
    check("note C plays ~261.63 Hz (C4)", abs(L.note_to_freq("C") - 261.63) < 0.5)
    check("a rest is silent (0 Hz)", L.note_to_freq("rest") == 0.0)

    # ---- friendly errors ----
    r = L.run_code('t = Turtle(\nt.forward(10)')
    check("syntax error reported with a line", not r["ok"] and r["error"]["type"] == "SyntaxError")

    r = L.run_code('t = Turtle()\nt.forward("oops")')
    check("runtime error reports the right line", not r["ok"] and r["error"]["line"] == 2)

    r = L.run_code('fowrard(100)')
    check("NameError suggests 'forward' for 'fowrard'",
          not r["ok"] and "forward" in (r["error"].get("friendly") or ""))

    r = L.run_code('t = Turtle()\nt.fowrard(100)')
    check("AttributeError suggests 'forward' for t.fowrard",
          not r["ok"] and "forward" in (r["error"].get("friendly") or ""))

    # ---- the infinite-loop guard (this one runs the watchdog; takes a moment) ----
    r = L.run_code('while True:\n    x = 1')
    check("endless loop is stopped (not frozen)", not r["ok"] and r["error"]["type"] == "RuntimeError")

    # ---- lessons are well-formed ----
    check("there are 27 lessons", len(L.LESSONS) == 27)
    transitions = sum(1 for i in range(len(L.LESSONS)) if i == 0 or L.LESSONS[i]["track"] != L.LESSONS[i - 1]["track"])
    check("lessons form 5 contiguous track groups", transitions == 5)
    for les in L.LESSONS:
        ok = all(k in les for k in ("track", "title", "goal", "tip", "code"))
        check("lesson has all fields: %s" % les.get("title", "?"), ok)

    # ---- every maze is well-formed AND solvable ----
    mazes = [x for x in L.LESSONS if x.get("maze")]
    for m in mazes:
        mz = m["maze"]
        rows = mz["rows"]
        C = len(rows[0])
        sr, sc = mz["start"]
        gr, gc = mz["goal"]
        wf = (all(len(row) == C for row in rows) and rows[sr][sc] == "." and rows[gr][gc] == "." and (sr, sc) != (gr, gc))
        check("maze well-formed: %s" % m["title"], wf)

    # spot-check the named puzzles are solvable with their intended solutions
    F = lambda n: ["forward"] * n  # noqa: E731
    by = {m["title"]: m["maze"] for m in mazes}
    check("'Straight to the star' solvable", maze_solves(by["Straight to the star"], F(4)))
    check("'Around the corner' solvable", maze_solves(by["Around the corner"], F(2) + ["right"] + F(2)))
    check("'Turn left this time' solvable", maze_solves(by["Turn left this time"], F(2) + ["left"] + F(2)))
    check("'Climb the staircase' solvable", maze_solves(by["Climb the staircase"], ["forward", "left", "forward", "right"] * 4))

    print()
    if _fails:
        print("❌ %d check(s) FAILED" % _fails)
        sys.exit(1)
    print("✅ all checks passed")


if __name__ == "__main__":
    main()
