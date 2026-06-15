# Module 2 — Shapes 🔺🟦

**For the grown-up.** Module 1 was about single steps in order. Now we combine
those steps into whole shapes, and combine shapes into a picture.

---

## The Big Idea
> Big, complicated things are built out of small, simple things you already
> know. A house is just a square plus a triangle.

This is called **decomposition** (breaking a big problem into smaller ones) — a
superpower that real programmers use every single day.

## What your child will learn
- Shapes are made of **sides + turns** repeated.
- A bigger picture (a house) is made of **smaller shapes** (square + triangle).
- How to **lift the pen** to move without drawing a line.

## Time
About **20 minutes**.

---

## Warm-up (no computer) — "Shape hunt" 🔍
Walk around the room for 2 minutes and find shapes: the TV is a rectangle, a
plate is a circle, a slice of pizza is a triangle. Then ask: *"What shapes is a
house made of?"* Draw a quick house on paper together and point to the square
and the triangle. That's exactly what the code will do.

---

## Let's code together

```
python3 02_shapes/1_triangle.py
python3 02_shapes/2_a_house.py
python3 02_shapes/3_your_picture.py
```

1. **`1_triangle.py`** — Same idea as the square, but 3 sides and a bigger turn
   (120 instead of 90). Count the sides as it draws.
2. **`2_a_house.py`** — Watch carefully: first it draws the **square** walls,
   then it **lifts the pen** (no line!) to move up, then draws the **triangle**
   roof. Pause and point out the moment the pen lifts.
3. **`3_your_picture.py`** — This one is a blank canvas. There's a **menu of
   commands** at the top of the file. Pick some together and build anything.

> 💡 **Tip:** Open `3_your_picture.py` in any text editor (even TextEdit). Let
> your child *tell you* what to add — "make it blue!", "do a big dot!" — and you
> type it. They are programming; you are just the keyboard.

---

## Talk about it
- "What two shapes make a house?"
- "Why did the turtle lift its pen? What would happen if it didn't?" (Try
  deleting the `t.penup()` line in the house and run it — a stray line appears!)
- "What shape could we add next? A sun (dot)? A path (line)?"

## Little challenges
- 🟢 **Easy:** Change the house colors. A purple house with a green roof?
- 🟡 **Medium:** In `3_your_picture.py`, draw a **sun**: use `t.penup()`, move to
  a corner, `t.pendown()`, then `t.dot(60, "gold")`.
- 🔴 **Spicy:** Add a **door** to the house — a small square or just a thick
  short line near the bottom.

---

## Words we learned
| Word | Kid-friendly meaning |
|------|----------------------|
| **shape** | sides and turns that make a closed picture |
| **decompose** | break a big thing into smaller, easier things |
| **pen up / pen down** | move without drawing / draw while moving |
| **dot** | a round stamp of color |

## If something goes wrong 🛟
- **The roof looks wonky after you changed wall sizes?** That's expected! The
  roof numbers were measured for the original walls. Experimenting and getting a
  funny result *is* learning — adjust the roof numbers and try again.
- **A line appears where you didn't want one?** You probably moved while the pen
  was down. Add `t.penup()` before the move and `t.pendown()` after.

> ⭐ **Done!** Next up: **Module 3 — Loops**, the magic shortcut for "do this
> again and again."
