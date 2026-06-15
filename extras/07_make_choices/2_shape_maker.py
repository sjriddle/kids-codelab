# The Shape Maker! 🔷
# YOU tell the program how many sides you want, and it draws that shape.
# The program listens to you (input) and reacts (draws). It even does a little
# math: the corner turn is always 360 divided by the number of sides.

# --- this little block helps Python find our drawing helper ---
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# --------------------------------------------------------------
from kidturtle import Turtle

print("\n🔷 Welcome to the Shape Maker! 🔷")

# Ask how many sides. We try to turn the answer into a number.
answer = input("How many sides should your shape have? (try 3 to 8): ").strip()

if answer.isdigit() and int(answer) >= 3:
    sides = int(answer)
else:
    print("Hmm, I'll pick 5 sides for you!")
    sides = 5  # a friendly fallback so the program always works

# Ask for a color, with a safe default.
color = input("What color? (like red, blue, green, gold): ").strip().lower()
if color == "":
    color = "purple"

# The math trick: all the corner turns add up to one full turn (360 degrees).
turn = 360 / sides

t = Turtle()
t.color(color)
t.width(6)

for side in range(sides):
    t.forward(160)
    t.right(turn)

names = {
    3: "triangle",
    4: "square",
    5: "pentagon",
    6: "hexagon",
    7: "heptagon",
    8: "octagon",
}
shape_name = names.get(sides, "shape")
print("Drawing your " + color + " " + shape_name + "! 🎨")

t.show("My " + shape_name.title())

# 🔧 TRY THIS:
#   - Run it a few times with different numbers. 8 sides? 12? 20 (almost a circle)!
#   - What happens with a really big number, like 30?
