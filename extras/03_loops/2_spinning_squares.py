# Spinning squares! 🌀
# A loop INSIDE a loop. We draw a square, turn a little, and do it again...
# and again... until the squares make a beautiful spinning pattern.

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.color("magenta")
t.width(2)

# The OUTER loop: do this whole thing 12 times.
for spin in range(12):
    # The INNER loop: draw one square (4 sides).
    for side in range(4):
        t.forward(140)
        t.right(90)
    # After each square, turn a little before drawing the next one.
    t.right(30)  # 12 squares × 30 degrees = a full 360 spin!

t.show("Spinning Squares")

# 🔧 TRY THIS:
#   - Change the color to "blue" or "darkorange".
#   - Change range(12) to range(18) and t.right(30) to t.right(20).
#   - Swap the square (inner loop) for a triangle: range(3) and right(120).
