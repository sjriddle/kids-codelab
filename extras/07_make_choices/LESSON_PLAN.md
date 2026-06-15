# Module 7 — Make Choices 🔀

**For the grown-up.** The final core idea: **decisions**. Until now the program
always did the same thing. Now it chooses what to do based on the answer it's
given. This is the `if` statement — the foundation of all "smart" behavior in
software.

---

## The Big Idea
> A program can **make a decision**: *IF* this is true, do one thing, *OTHERWISE*
> do something else.

## What your child will learn
- `if` / `elif` / `else` — the program picks a path based on the answer.
- A program can **combine everything**: input + decisions + drawing + math.
- Their choices change what the computer does. They're in control.

## Time
About **15–20 minutes**.

---

## Warm-up (no computer) — "If... then..." game 🎭
Play a quick round of "If... then...": *"If I clap, you jump. Otherwise, you
freeze."* Do a few. Then make it sillier: *"IF I say 'banana', do a dance.
ELSE, touch your nose."* Your child is running `if`/`else` with their body. That
is exactly what the code does.

---

## Let's code together

```
python3 07_make_choices/1_magic_door.py
python3 07_make_choices/2_shape_maker.py
```

1. **`1_magic_door.py`** — The program asks which door to open and shows a
   **different** result for **red**, **blue**, or anything else. Play it a few
   times choosing different doors so they see the `if` choosing the path.
2. **`2_shape_maker.py`** — Your child decides how many sides and what color, and
   the program **draws exactly that** in the browser. Try 3, then 6, then 12.
   Point out: more sides looks more like a circle! (This quietly ties together
   loops, input, decisions, and a touch of math.)

---

## Talk about it
- "What made door one different from door two?" (The `if` checked your answer.)
- "What happens if you type something that isn't red or blue?" (The `else`
  catches it — the silly goose!)
- "What's your favorite number of sides? Let's draw it."

## Little challenges
- 🟢 **Easy:** Change what's behind each magic door.
- 🟡 **Medium:** Add a **green** door to the adventure with another `elif`
  (copy the blue block and change `blue` to `green` and the story).
- 🔴 **Spicy:** In the Shape Maker, make the shape **bigger when there are more
  sides** — that's a real "if" decision your child can design with you.

---

## Words we learned
| Word | Kid-friendly meaning |
|------|----------------------|
| **if** | do something only when the answer matches |
| **else** | what to do when it doesn't match |
| **decision** | the program choosing between paths |
| **condition** | the thing we check (like "is it red?") |

## If something goes wrong 🛟
- **Typed the answer but nothing happened?** Make sure you pressed **Enter**.
- **Red error after typing a color?** Color names should be one word with no
  spaces: `hotpink`, `skyblue`, `red`. If a color isn't recognized the shape may
  not show — just run it again with a simpler color.
- **Want to quit a question?** Press **Ctrl + C**.

> 🏆 **You finished the whole course!** Your child has met the five big ideas of
> coding: **sequence, loops, lists/variables, interaction, and decisions.**
> See the main `README.md` for "what's next" ideas.
