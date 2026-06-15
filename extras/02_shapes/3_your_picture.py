# Your picture! 🎨
# This file is YOURS to play with. Mix and match the commands below.
# There is no wrong answer — just make something fun!

# --- this little block helps Python find our drawing helper ---
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()

# Here is a menu of commands you can copy and use as many times as you want:
#
#     t.color("red")      <- change the pen color
#     t.width(10)         <- change how thick the line is
#     t.forward(100)      <- walk forward
#     t.backward(100)     <- walk backward
#     t.left(90)          <- turn left
#     t.right(90)         <- turn right
#     t.dot(30)           <- stamp a dot
#     t.penup()           <- lift the pen (move without drawing)
#     t.pendown()         <- put the pen down again
#
# A starter drawing is below. Change it, add to it, or erase it and start fresh!

t.color("orange")
t.width(8)
t.forward(120)
t.dot(40, "purple")
t.left(120)
t.forward(120)
t.dot(40, "green")

t.show("My Own Picture")
