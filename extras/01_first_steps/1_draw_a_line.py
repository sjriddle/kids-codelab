# Draw a line!
# This is the very first program. It tells the turtle to walk forward.

# --- this little block helps Python find our drawing helper ---
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()          # Wake up a turtle. It starts in the middle.

t.color("blue")       # Pick a pen color.
t.forward(200)        # Walk forward 200 steps, drawing as it goes.

t.show("My First Line")   # Open the browser and watch it draw!

# 🔧 TRY THIS:
#   - Change 200 to a bigger number, like 300. What happens?
#   - Change "blue" to "red" or "green".
