# 🧪 The Code Lab — Teaching Guide

**For the grown-up.** The Code Lab is the whole course in one browser page. Your
child picks a lesson, reads the goal, and plays by turning **knobs** or editing
**code** — and the result draws, plays music, animates, or becomes a little game.
No text editor, no file hunting, no setup beyond one command.

```
python3 code_lab/code_lab.py
```

When you're done, press **Ctrl + C** in the Terminal.

---

## How a lesson works
1. **Pick a lesson** from the dropdown (they're grouped by track).
2. **Read the goal** — the yellow banner says what to try.
3. **Open the 💡 Grown-up tip** for an unplugged warm-up and what to ask.
4. **Play:** drag a **knob**, or change the **code**, then press **▶ Run** (or
   **Enter**). Use **Next ▶** to move on and **↺** to reset a lesson.

> 🔑 **The magic moment:** when your child drags a knob, the matching line of code
> **lights up**. Point at it and say the variable's name together. That link —
> "this knob *is* this word in the code" — is the whole game.

---

## Helpful buttons & options
- **🔊 (next to the goal)** reads the goal out loud — great before your child can
  read fluently.
- **➕ Add buttons** (above the code) insert a real line of code with one tap — a
  gentle on-ramp for kids who can't type yet, between knobs and typing.
- **💾 Save picture** downloads their creation; finishing a lesson earns a **⭐**
  (see the count up top), and their edits are remembered when they return.
- **🌙 Calm** (top right) turns off confetti/pops/sounds for a quieter session;
  it also switches on by itself if your device is set to "reduce motion."
- **↺** restores a lesson's original code if things get tangled.
- If something breaks, the message **names the line and suggests a fix**, and the
  broken line glows red — a perfect "let's debug together" moment.
- On a tablet: start with `python3 code_lab/code_lab.py --lan` (see `SETUP.md`);
  the **on-screen arrows** appear for the Play track so no keyboard is needed.

## The five tracks (what each teaches + how to guide it)

### 🎨 Draw — *sequence, loops, variables, lists*
The classic turtle drawing. Start with **A square** (a loop), then **Any shape**
(change `sides` to morph triangle → pentagon → circle), then **A flower**.
- **Unplugged:** walk a square together — "forward, turn" four times. A loop just
  says "do it 4 times."
- **Ask:** "How many sides? How big a turn?" (It's always 360 ÷ sides.)

### 🎵 Music — *sequences & loops you can HEAR*
Code that plays notes. **First notes** (change a letter A–G), **A loop tune**
(repeat with a loop), **Twinkle Twinkle** (a real melody from a **list**).
- **Unplugged:** clap a rhythm and repeat it — that's a loop with sound.
- **Ask:** "What happens if we change the order of the notes?" (Sequence matters!)
- 🔈 Make sure the volume is up; press Run once so the browser allows sound.

### 🤖 Maze — *algorithms & debugging*
Steer a robot to the ⭐. **Straight to the star** (how many steps?), **Around the
corner** (turn, then go), **The long hallway** (use a loop!).
- This is the best track for real **algorithmic thinking**: the starter code is
  *deliberately not finished*. Too few steps and you stop short; too many and you
  bonk a wall. Fixing the number/turns **is debugging**.
- **Ask:** "Count the cells. How many forwards? Where do we turn?"
- 🎉 Reaching the star sets off **confetti and a happy chime** — a real reward for
  solving the puzzle. (Finishing any other lesson gives a cheerful "pop" too.)

### 🏃 Move — *things change over time*
Simple animations. **Fly the rocket**, **Bouncing ball**, **A little scene** with
two characters.
- **Unplugged:** flip a stack of slightly-different drawings (a flip-book) — many
  small changes make motion.
- **Ask:** "What makes it move smoothly? What if each hop is bigger?"

### 🕹️ Play — *events: the program reacts to YOU*
Interactive programs. **Drive the car** (arrow keys), **Magic star** (click).
- After you press Run, **click the picture** so it's listening, then use the keys.
- **Unplugged:** play "if I clap, you jump" — that's an event + a response, just
  like `on_key`.
- **Ask:** "How does it know which arrow you pressed?"

---

## 🎪 Free-play sandboxes
Every track ends with a **🎪 Free play** lesson — a blank-ish starter with a
**command menu** (a list of every command, ready to copy) right there in the code.
There's no goal to "get right": it's open-ended making. These are perfect when
your child has the idea and just wants to build — a drawing of anything, their own
song, a roaming robot, a moving scene, or a little game with their favorite emoji.
Read the menu together and let them point to what to try next.

## Little challenges that work in any track
- 🟢 Change one knob and predict the result before letting go.
- 🟡 Change a number in the code by hand, then press Run.
- 🔴 Combine ideas — a longer song, a two-character scene, a trickier path.

## Words we learn
| Word | Kid-friendly meaning |
|------|----------------------|
| **sequence** | doing steps in order |
| **loop** | repeat steps without rewriting them |
| **variable** | a named knob you can change |
| **list** | a collection of things (notes, colors) in `[ ]` |
| **algorithm** | a plan of steps to reach a goal |
| **event** | something happening, like a key press or a click |
| **debug** | find and fix what's wrong |

## If something goes wrong 🛟
- **A red message in the black box?** That's an error with the line number — read
  it together, fix it, Run again, or press **↺** to reset the lesson.
- **Knobs didn't appear?** They're made for simple lines like `size = 150` or
  `color = "blue"` at the start of the code. After editing by hand, press **▶ Run**
  to refresh them.
- **No sound?** Press Run once (a click/keypress lets the browser play), check the
  volume.
- **Game keys don't work?** Click the picture first so it's focused (it gets a
  yellow outline), then press the arrow keys.
- **Page won't load / frozen?** Make sure the Code Lab is still running in the
  Terminal; if not, start it again. A `while True` with no drawing can hang it —
  press **Ctrl + C** and restart.

> ⭐ This one page grows with your child: today they turn knobs, soon they edit
> code, and one day they'll write their own lessons from scratch.
