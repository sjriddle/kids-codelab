# A flower! 🌸
# Each petal is a circle. We draw a circle, turn a bit, draw another...
# Loops turn a boring repeat into a beautiful flower.

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.color("deeppink")
t.width(2)

# Draw 9 petals all the way around.
for petal in range(9):
    t.circle(70)  # draw one round petal
    t.right(40)  # 9 petals × 40 degrees = a full circle of petals

# Put a sunny dot in the middle.
t.dot(40, "gold")

t.show("My Flower")

# 🔧 TRY THIS:
#   - More petals: range(12) with t.right(30).
#   - A different petal size: change circle(70) to circle(50) or circle(100).
#   - Change "deeppink" to your favorite color, and the middle "gold" too.
