# Draw a triangle!
# A triangle has 3 sides. At each corner the turtle turns the SAME amount.

# --- this little block helps Python find our drawing helper ---
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.color("red")
t.width(6)

t.forward(180)        # side 1
t.left(120)           # turn
t.forward(180)        # side 2
t.left(120)           # turn
t.forward(180)        # side 3

t.show("My Triangle")

# 🔧 TRY THIS:
#   - Change all three 180s to 100 for a smaller triangle.
#   - A square turns 90 each corner. A triangle turns 120. Can you guess why?
#     (Hint: the turns always add up to one full spin = 360!)
