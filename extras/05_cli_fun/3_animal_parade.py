# Animal parade! 🐢🐰🐢
# Watch the animals march across the Terminal, one after another.
# The trick: print the animal, move it one space to the right, repeat.

import time

CYAN = "\033[96m"
BOLD = "\033[1m"
END = "\033[0m"

print(CYAN + BOLD + "\n   🎺 The Animal Parade is starting! 🎺\n" + END)
time.sleep(1)

# A list of animals that will each take a turn marching.
animals = ["🐢", "🐰", "🦆", "🐱", "🐢", "🦖"]

steps_across = 35  # how far each animal walks

for animal in animals:
    for position in range(steps_across):
        spaces = " " * position
        # "\r" jumps back to the start of the line so we can redraw it.
        # end="" and flush=True make the animation smooth.
        print("\r" + spaces + animal, end="", flush=True)
        time.sleep(0.05)
    print()  # finish this animal's line and start a new one

print(BOLD + "\n   🏁 The parade is over! Take a bow! 🐢\n" + END)

# 🔧 TRY THIS:
#   - Change the animals in the list, or add more.
#   - Make them march slower: change 0.05 to 0.1.
#   - Make the parade longer: change steps_across to 50.
