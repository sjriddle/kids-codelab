# Rainbow spiral! 🌈
# We keep a LIST of colors and use a new one each time around the loop.
# A little longer each step makes it spiral outward.

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.width(4)

# A LIST is a bunch of things kept together, inside [ ].
rainbow = ["red", "orange", "gold", "green", "blue", "purple"]

length = 5  # how long the next line will be (it grows!)

for step in range(60):
    # Pick a color from the list, looping back to the start when we run out.
    # (len(rainbow) is just "how many colors are in the list".)
    color = rainbow[step % len(rainbow)]
    t.color(color)
    t.forward(length)
    t.right(59)  # a tiny bit less than 60 makes it spiral
    length = length + 4  # each line is a little longer than the last

t.show("Rainbow Spiral")

# 🔧 TRY THIS:
#   - Change right(59) to right(91) for a square-ish spiral.
#   - Change range(60) to range(120) for a giant spiral.
#   - Make your own color list! Try ["hotpink", "cyan", "yellow"].
