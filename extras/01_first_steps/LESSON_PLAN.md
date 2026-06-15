# Module 1 — First Steps 🐢

**For the grown-up helping out.** You run the scripts and read the comments; your
child watches, predicts, and decides what numbers to change. Reading is *not*
required — this is about ideas, not typing.

---

## The Big Idea
> A program is a list of instructions, and the computer does them **in order**,
> one at a time, from top to bottom.

This is the single most important idea in all of coding. Everything else is
built on it.

## What your child will learn
- A computer follows instructions **one step at a time**.
- The **order** of the steps changes the result.
- Two turtle ideas: **forward** (move) and **turn** (left / right).

## Time
About **15–20 minutes**. For this age, stop while it's still fun.

## What you need
- The Terminal app (already open, since you're here!).
- That's it — no installing anything.

---

## Warm-up (no computer) — "You be the robot" 🤖
Stand at one side of the room. Your child gives you instructions to reach a toy:
"3 steps forward... turn left... 2 steps forward." Follow them **exactly** and
literally (this is the funny part — if they say "turn" without saying which way,
turn in a silly circle!).

Then **swap**: you give the instructions, they are the robot.

**The point they should feel:** the robot only does *exactly* what it's told, in
the *exact order* it's told. That's how the turtle works too.

---

## Let's code together

Run each one by typing this into the Terminal (then press Enter):

```
python3 01_first_steps/1_draw_a_line.py
```

Then `2_make_a_path.py`, then `3_draw_a_square.py`.

A web page will pop open and the turtle will **draw the picture for you, slowly**,
so you can watch the order of the steps. Press **▶ Play again** to replay it.

1. **`1_draw_a_line.py`** — one single instruction: walk forward. Ask: *"How far
   do you think it will go?"* Then change `200` to a bigger number and run again.
2. **`2_make_a_path.py`** — walk, turn, walk, turn. **Before** you run it, trace
   the path in the air with your finger. Were you right?
3. **`3_draw_a_square.py`** — count the sides out loud *with* the turtle:
   "side one... turn... side two..."

---

## Talk about it (great questions to ask)
- "What does **forward** mean? What does **turn** mean?"
- "If I switch two lines around, will the picture change?" (Try it! Swap a
  `forward` with a `right` and see.)
- "How many sides does a square have? How many turns did the turtle make?"

## Little challenges (pick one)
- 🟢 **Easy:** Change the colors. Try `"hotpink"`, `"orange"`, `"skyblue"`.
- 🟡 **Medium:** In `2_make_a_path.py`, add more `forward` / `turn` lines to make
  the path longer.
- 🔴 **Spicy:** In the square, change every `right(90)` to `right(120)` and remove
  one side. What shape appears? (Hint: it has 3 sides!)

---

## Words we learned
| Word | Kid-friendly meaning |
|------|----------------------|
| **program** | a list of instructions for the computer |
| **instruction** | one thing to do, like "forward 100" |
| **in order** | doing the steps one after another, top to bottom |
| **forward** | move the turtle straight ahead |
| **turn (left/right)** | spin the turtle to face a new way |

## If something goes wrong 🛟
- **Nothing popped up?** Look in the Terminal — it prints the picture's file
  location. Copy that line into your browser's address bar.
- **A red error message?** Check the line it names for a missing `(` or `)` or a
  missing quote `"`. The most common fix is matching quotes: `"blue"` not `blue`.
- **Two turtles in two tabs?** That's fine — each run opens its own tab. Close
  the old ones whenever you like.

> ⭐ **Done!** Your child just told a computer what to do and watched it obey.
> Next up: **Module 2 — Shapes**, where the steps combine into pictures.
