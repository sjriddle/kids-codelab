# Module 6 — Browser Playground 🎨

**For the grown-up.** This module is a real little **web app** running on
`localhost` (your own computer acting as a tiny website). It's the most
free-play, creative module — pure fun, with a couple of "how does this work?"
ideas underneath.

---

## The Big Idea
> A program can be **interactive** — it waits for *you* to click, drag, and
> press, and responds right away. That's how every app and website works.

## What your child will learn
- What a **server** and **localhost** are (your computer talking to itself).
- A program can **react to clicks and movement** (events).
- Creative confidence: they're "using an app they ran themselves."

## Time
**Open-ended.** Could be 10 minutes or a happy half hour.

---

## Warm-up (no computer) — "Simon Says" 🙋
Play one quick round of Simon Says. The point: the program (you, "Simon")
**reacts to what the player does**. The playground reacts to clicks and drags the
same way — it's listening for what your child does and responding instantly.

---

## Let's start it up

```
python3 06_browser_playground/start_playground.py
```

Your browser opens to something like `http://localhost:8000`. That address means
"this very computer." You started a tiny web server, and your browser is visiting
it. 🎉

**In the playground your child can:**
- 🖍️ **Click and drag** on the white board to draw.
- 🎨 Tap a **color** circle, including the **🌈 rainbow** that changes as you draw.
- ⬤ Pick a **brush size** (small, medium, big).
- ⭐🐢❤️🌸🦖 Tap a **stamp**, then click to place emojis (tap **✏️ Draw** to go
  back to drawing lines).
- 🧽 **Clear** to start over, 💾 **Save** to download the masterpiece as a picture.

**When you're finished:** go back to the Terminal and press **Ctrl + C** to stop
the server.

---

## Talk about it
- "What does it mean that this is running on *our* computer?" (We made a tiny
  website just for us — that's `localhost`.)
- "How does it know where you're drawing?" (It's **listening** for your finger or
  mouse — that's called an **event**.)
- "What's your favorite tool? Let's make a picture of our family / pet / house."

## Little challenges (with grown-up help)
- 🟢 **Easy:** Draw a self-portrait and **Save** it. Find the saved picture in
  your Downloads folder.
- 🟡 **Medium:** Open `web/index.html` in a text editor and **add a new stamp** —
  copy a `<button class="stamp" ...>` line and change the emoji to a new one.
- 🔴 **Spicy:** In `web/index.html`, add a new **color** by copying a `<button
  class="swatch" ...>` line and changing the color code (try `#00bcd4`).

---

## Words we learned
| Word | Kid-friendly meaning |
|------|----------------------|
| **server** | a program that hands out web pages |
| **localhost** | your own computer, talking to itself |
| **interactive** | the program reacts to what you do |
| **event** | something happening, like a click or a drag |
| **save / download** | keep a copy of your picture as a file |

## If something goes wrong 🛟
- **Browser didn't open?** Look in the Terminal for the address (like
  `http://localhost:8000`) and type it into your browser yourself.
- **"Address already in use"?** The script automatically tries the next port
  number — just use the address it prints.
- **Can't stop it?** Click on the Terminal window first, then press **Ctrl + C**.
- **Drawing in the wrong spot?** Refresh the page (Cmd + R) and try again.

> ⭐ **Done!** One module to go: **Module 7 — Make Choices**, where the program
> makes decisions based on what you tell it.
