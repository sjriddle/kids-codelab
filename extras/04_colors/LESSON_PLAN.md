# Module 4 — Colors & Art 🌈

**For the grown-up.** Loops + color = the most rewarding module so far. We also
sneak in two real programming ideas: **lists** (a collection of things) and
**randomness** (the computer making surprises).

---

## The Big Idea
> We can keep a **collection** of things (a list of colors) and have the
> computer **choose** from it — even *randomly*, so we get surprises.

## What your child will learn
- A **list** holds many things together (like a box of crayons).
- The loop can pick a **different item each time** it goes around.
- **Random** lets the computer surprise us — different every run.

## Time
About **20 minutes**, but the art is addictive — they may want more.

---

## Warm-up (no computer) — "The crayon box" 🖍️
Get a box of crayons. Talk about how the box is **one thing** that holds **many**
colors — that's exactly what a **list** is in code. Then play a game: close your
eyes and pull out a crayon without looking. That surprise pick is **random**!

---

## Let's code together

```
python3 04_colors/1_rainbow_spiral.py
python3 04_colors/2_polka_dots.py
python3 04_colors/3_color_star.py
```

1. **`1_rainbow_spiral.py`** — A **list** of 6 colors; the loop uses the next one
   each time and makes each line a little longer, spiraling outward.
2. **`2_polka_dots.py`** — **Random** spots, sizes, and colors. **Run it three
   times** and watch it be different every time. This "why is it different?!"
   moment is gold.
3. **`3_color_star.py`** — The classic 5-point star (turn 144°), with a different
   color on each point.

---

## Talk about it
- "What's in our list of colors? Can we add one?"
- "Why did the polka dots come out different each time we ran it?" (Because it's
  **random** — the computer surprised us.)
- "How does the star know to make a point?" (The big 144° turn crosses the
  lines.)

## Little challenges
- 🟢 **Easy:** Build your own color list and watch the spiral/star change.
- 🟡 **Medium:** In the polka dots, make them all big: change the size range to
  `random.randint(40, 80)`.
- 🔴 **Spicy:** In the star file, follow the "spinning stars" hint at the bottom
  to make a whole galaxy of stars.

---

## Words we learned
| Word | Kid-friendly meaning |
|------|----------------------|
| **list** | a collection of things kept together, in `[ ]` |
| **variable** | a name that holds a value (like `length` or `color`) |
| **random** | the computer making a surprise choice |
| **choice** | picking one thing from a list |

## If something goes wrong 🛟
- **`IndexError`?** A list has, say, 6 colors but the code asked for the 8th.
  The spiral uses `% len(rainbow)` to avoid this — keep that part as-is when you
  change the color list.
- **It looks the same every run?** That's the spiral or star (not random). Only
  the polka dots use `random`, so only that one changes each time.

> ⭐ **Done!** Time to leave the drawing window. Next up: **Module 5 — CLI Fun**,
> where the *Terminal itself* becomes colorful and animated.
