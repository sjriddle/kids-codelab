# Make a path!
# The turtle walks, turns, walks, turns. Each line is ONE instruction.
# Computers do instructions IN ORDER, from top to bottom.

# --- this little block helps Python find our drawing helper ---
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.color("purple")
t.width(8)            # A nice thick crayon line.

t.forward(120)        # walk
t.left(90)            # turn left (a quarter turn)
t.forward(120)        # walk
t.right(90)           # turn right
t.forward(120)        # walk
t.left(90)            # turn left
t.forward(120)        # walk

t.show("My Staircase Path")

# 🔧 TRY THIS:
#   - Add two more lines at the bottom (before t.show) to make the path longer:
#         t.right(90)
#         t.forward(120)
#   - Change some 90s to 45 to make gentler turns.
