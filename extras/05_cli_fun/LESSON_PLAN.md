# Module 5 — CLI Fun 💻

**For the grown-up.** A change of scenery from the drawing window: these programs
run right in the **Terminal** (the "CLI" = Command Line Interface). Kids see that
code can also **talk to you**, **count**, and **animate text**.

---

## The Big Idea
> A program can do more than draw. It can **ask you questions**, **count**, and
> **wait** — and show it all in colorful text.

## What your child will learn
- Programs can **take input** (ask you something) and **respond**.
- `time.sleep` makes the computer **wait** — that's how we animate.
- Counting and lists power simple animations.

## Time
About **15 minutes**.

---

## Warm-up (no computer) — "Countdown!" 🚀
Do a real countdown together: "5... 4... 3... 2... 1... BLAST OFF!" and jump up.
Talk about how each number waits a moment before the next — *the waiting is part
of the fun.* The rocket program does exactly this with `time.sleep`.

---

## Let's code together

```
python3 05_cli_fun/1_hello_with_color.py
python3 05_cli_fun/2_counting_rocket.py
python3 05_cli_fun/3_animal_parade.py
```

1. **`1_hello_with_color.py`** — It will **ask for a name**. Let your child say
   it; you type it and press **Enter**. Watch their name appear in rainbow
   letters. (This is "input" — the program listening to us.)
2. **`2_counting_rocket.py`** — A countdown using a loop, then a rocket that
   flies up the screen. Count along out loud!
3. **`3_animal_parade.py`** — Animals march across the Terminal. The smooth
   motion comes from drawing, waiting a tiny bit, and redrawing.

> 🛑 **To stop any Terminal program early**, press **Ctrl + C** (hold Control,
> tap C). Good to know for the longer animations.

---

## Talk about it
- "How did the computer know your name?" (We *told* it — that's input.)
- "What makes the rocket move slowly instead of all at once?" (It **waits** a
  little between steps — `time.sleep`.)
- "What's the same about the parade and the countdown?" (Both use a **loop** to
  repeat.)

## Little challenges
- 🟢 **Easy:** Change the animals in the parade list to your favorites.
- 🟡 **Medium:** Make the countdown start from 10.
- 🔴 **Spicy:** In `1_hello_with_color.py`, ask a **second** question (like a
  favorite animal) with another `input(...)` and use it in the greeting.

---

## Words we learned
| Word | Kid-friendly meaning |
|------|----------------------|
| **CLI / Terminal** | the text window where we type commands |
| **input** | information we give the program (like our name) |
| **sleep / wait** | the program pauses for a moment |
| **animation** | moving pictures made by redrawing quickly |

## If something goes wrong 🛟
- **The program seems stuck?** It might be **waiting for you to type** and press
  Enter (the hello program does this). Type something and hit Enter.
- **Want to quit?** Press **Ctrl + C**.
- **Emojis look like boxes?** Some terminals show certain emojis differently —
  that's okay, the program still works. Try different emojis.

> ⭐ **Done!** Next up: **Module 6 — Browser Playground**, a real `localhost`
> web page where your child draws by clicking and pressing keys.
