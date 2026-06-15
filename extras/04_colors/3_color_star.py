# A color-changing star! ⭐
# A star is 5 long points. The big turn of 144 degrees makes the points cross.
# We change color on every point so it's a rainbow star.

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

t = Turtle()
t.width(5)

star_colors = ["red", "gold", "limegreen", "deepskyblue", "violet"]

for point in range(5):
    t.color(star_colors[point])  # a new color for each of the 5 points
    t.forward(250)
    t.right(144)  # the magic star angle!

t.show("Rainbow Star")

# 🔧 TRY THIS:
#   - Change the 5 colors in the list to your favorites.
#   - Make a bigger star: change 250 to 320.
#   - Spicy: wrap the whole thing in another loop to make spinning stars:
#         for spin in range(6):
#             (put the star loop here, indented more)
#             t.right(60)
