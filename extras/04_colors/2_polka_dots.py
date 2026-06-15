# Polka dots! 🔴🟡🔵
# The computer can make surprises using RANDOM. Every time you run this,
# the dots land in different spots with different colors and sizes!

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle
import random  # the "surprise" helper

t = Turtle()

colors = ["red", "orange", "gold", "green", "blue", "purple", "hotpink", "cyan"]

for dot in range(25):
    t.penup()  # lift pen so we don't draw lines
    x = random.randint(-250, 250)  # a surprise left-right spot
    y = random.randint(-200, 200)  # a surprise up-down spot
    t.goto(x, y)  # jump there
    size = random.randint(20, 60)  # a surprise size
    color = random.choice(colors)  # pick any color at random
    t.dot(size, color)  # stamp it!

t.show("Polka Dots")

# 🔧 TRY THIS:
#   - Run it three times. It's different every time! Why? (random = surprise)
#   - Change range(25) to range(60) for LOTS of dots.
#   - Add your own colors to the list.
