# Draw a house!
# A house is a SQUARE with a TRIANGLE roof on top.
# See how we build a big picture out of shapes we already know?

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.width(6)

# ---- the walls (a square) ----
t.color("saddlebrown")
t.forward(150)  # bottom
t.left(90)
t.forward(150)  # right wall
t.left(90)
t.forward(150)  # top of the walls
t.left(90)
t.forward(150)  # left wall
t.left(90)  # now the turtle faces along the bottom again

# ---- move up to the top-left corner to start the roof ----
t.penup()  # lift the pen so we don't draw while moving
t.forward(0)
t.left(90)
t.forward(150)  # go up the left wall
t.right(90)
t.pendown()  # put the pen back down

# ---- the roof (a triangle) ----
t.color("red")
t.forward(150)  # the bottom of the roof (left to right)
t.left(135)
t.forward(106)  # up the right slope to the rooftop point
t.left(90)
t.forward(106)  # down the left slope, back to where we started

t.show("My House")

# 🔧 TRY THIS:
#   - Change the wall color "saddlebrown" to "skyblue".
#   - Make a taller house: change the four wall 150s to 200 (the roof may need
#     a tweak — that's part of the fun of experimenting!).
