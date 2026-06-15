# Draw a square!
# A square has 4 sides. So we say "forward, turn" 4 times.
# (In Module 3 we will learn a shortcut called a LOOP to do this faster!)

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.color("green")
t.width(6)

t.forward(150)  # side 1
t.right(90)  # turn the corner
t.forward(150)  # side 2
t.right(90)  # turn the corner
t.forward(150)  # side 3
t.right(90)  # turn the corner
t.forward(150)  # side 4

t.show("My Square")

# 🔧 TRY THIS:
#   - Count out loud with your turtle: "side 1, turn... side 2, turn..."
#   - Make a BIG square: change every 150 to 250.
#   - What happens if you change 90 to 120 and only draw 3 sides? (A triangle!)
