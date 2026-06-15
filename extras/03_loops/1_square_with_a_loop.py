# A square... with a LOOP!
# Remember the square in Module 1? We wrote "forward, turn" FOUR times.
# A loop says: "do this 4 times" — much shorter, and no copy-pasting!

# --- this little block helps Python find our drawing helper ---
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.color("teal")
t.width(6)

# "for ... in range(4):" means "repeat the indented lines 4 times."
for side in range(4):
    t.forward(150)    # walk one side
    t.right(90)       # turn the corner
    # ^ These two lines run 4 times. That's a whole square!

t.show("Square Made With a Loop")

# 🔧 TRY THIS:
#   - Change range(4) to range(3) and right(90) to right(120). A triangle!
#   - Change range(4) to range(5) and right(90) to right(72). A pentagon!
#   - The secret: the turn is always 360 divided by the number of sides.
