# 🛠️ Setup — open the Code Lab in 3 steps

This takes about two minutes. You only do it once to get comfortable; after that,
starting the Code Lab is a single line.

---

## Step 1 — Open the Terminal

The **Terminal** is a text window where you type commands.

- Press **Cmd + Space** (the magnifying glass / Spotlight) and type
  **`Terminal`**, then press **Enter**.
- A window with text and a blinking cursor appears. That's it!

---

## Step 2 — Go into this folder

In the Terminal, type `cd ` (the letters c-d and a space), then **drag the
`learn-to-code-kids` folder** from Finder onto the Terminal window (this pastes
its location), then press **Enter**.

It will look something like:

```
cd /Users/peechcraft/Code/learn/learn-to-code-kids
```

> ✅ **Check you're in the right place:** type `ls` and press Enter. You should
> see `README.md`, `code_lab`, and an `extras` folder.

---

## Step 3 — Start the Code Lab

Type this and press **Enter**:

```
python3 code_lab/code_lab.py
```

🎉 Your web browser pops open with the Code Lab. Pick a lesson from the dropdown,
read the goal, then **wiggle the knobs** or **change the code** and press
**▶ Run**. That's the whole thing!

When you're done, come back to the Terminal and press **Ctrl + C** to stop it.

---

## That's the whole routine

Every time you want to play, it's just:

```
python3 code_lab/code_lab.py
```

💡 **Tip:** type `python3 code` then press the **Tab** key to auto-complete the
rest. Saves typing.

---

## Good things to know

- **To stop the Code Lab**, click the Terminal window and press **Ctrl + C**
  (hold Control, tap C).
- **Each time you start it**, it opens a fresh browser tab. Close old ones
  whenever you like.
- **You don't need a separate text editor** — all the code editing happens right
  in the Code Lab page.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `python3: command not found` | Python isn't installed. Get it free at [python.org/downloads](https://www.python.org/downloads/), install, then reopen the Terminal. |
| `No such file or directory` | You're not in the right folder, or the path is mistyped. Redo Step 2, then use **Tab** to auto-complete. |
| Browser didn't open | Look in the Terminal for an address like `http://localhost:8050` and type it into your browser yourself. |
| `Address already in use` | The Lab automatically tries the next port — just use the address it prints. |
| No sound in the Music lessons | Press ▶ Run once (a click/keypress lets the browser play audio), and check the volume. |

Now head to **`README.md`** for the tour, or just start the Code Lab and explore.
Have fun! 🐢
