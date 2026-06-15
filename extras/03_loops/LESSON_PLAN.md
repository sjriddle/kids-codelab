# Module 3 — Loops 🔁

**For the grown-up.** This is a big one. Loops are where kids feel real
*power* — a tiny bit of code makes a huge, beautiful result. Lean into the "wow."

---

## The Big Idea
> When you need to do the same thing over and over, you don't write it over and
> over. You use a **loop**: "do this **N** times."

## What your child will learn
- A **loop** repeats instructions without copy-pasting them.
- `range(4)` means "do it 4 times."
- A loop **inside** a loop makes amazing patterns from very little code.

## Time
About **20 minutes**. The patterns are mesmerizing — let them watch and replay.

---

## Warm-up (no computer) — "The chorus" 🎵
Sing a song with a repeating chorus ("Row, row, row your boat" or "Baby Shark").
Point out: we don't write "doo doo doo" a hundred times — we just say *"sing the
chorus again!"* That instruction-to-repeat **is** a loop.

Or: clap a pattern (clap-clap-stomp) and say *"do that 3 times."* You just spoke
a loop out loud.

---

## Let's code together

```
python3 03_loops/1_square_with_a_loop.py
python3 03_loops/2_spinning_squares.py
python3 03_loops/3_flower.py
```

1. **`1_square_with_a_loop.py`** — Same square as Module 1, but only **two**
   lines do the work, wrapped in `for side in range(4):`. Show them the old
   square code side-by-side if you can — same picture, way less code!
2. **`2_spinning_squares.py`** — A loop **inside** a loop. The inside loop draws
   one square; the outside loop spins and repeats it 12 times. Watch the pattern
   bloom.
3. **`3_flower.py`** — Petals made from circles in a loop. Then a dot for the
   center.

> 🔑 **The indent matters.** The lines that are *pushed in* (indented) under the
> `for` line are the ones that repeat. If your child changes this file, keep the
> indentation lined up. (You don't have to explain this — just keep the spacing.)

---

## Talk about it
- "How many times does this loop repeat?" (Read the number in `range(...)`.)
- "What would 100 squares look like? Let's try `range(100)`!" (Do it — it's
  fast and gorgeous.)
- "Which is easier: writing 'forward, turn' 4 times, or saying 'do it 4 times'?"

## Little challenges
- 🟢 **Easy:** Change every `range(...)` number and watch the pattern change.
- 🟡 **Medium:** Turn the spinning squares into spinning triangles (inner loop:
  `range(3)` and `right(120)`).
- 🔴 **Spicy:** Make a "magic rule": the turn in `1_square_with_a_loop.py` should
  always be **360 ÷ number of sides**. Try 6 sides with `range(6)` and
  `right(60)` — a hexagon!

---

## Words we learned
| Word | Kid-friendly meaning |
|------|----------------------|
| **loop** | repeat instructions over and over |
| **range(4)** | "do it 4 times" |
| **repeat** | do the same thing again |
| **pattern** | something that repeats in a regular way |

## If something goes wrong 🛟
- **`IndentationError`?** The indented lines under `for` must all start with the
  same spaces. Easiest fix: undo your change and retype it carefully, keeping the
  spacing identical to the other lines.
- **It drew only part of the shape?** Check that the `for ... :` line ends with a
  colon `:` and the lines below it are indented.

> ⭐ **Done!** Your child just made a computer do 48 things by writing 4 lines.
> Next up: **Module 4 — Colors & Art**, where loops + colors = real artwork.
