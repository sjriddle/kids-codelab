# Hello, with color! 🌈
# This program talks to YOU. It asks your name and says hi in rainbow colors.
# It runs right here in the Terminal — no browser needed.

import time

# These are secret codes that turn the text different colors in the Terminal.
RED     = "\033[91m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
CYAN    = "\033[96m"
BLUE    = "\033[94m"
PURPLE  = "\033[95m"
BOLD    = "\033[1m"
END     = "\033[0m"     # this one turns the color back to normal

rainbow = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE]

# Ask the child (or grown-up) to type a name, then press Enter.
name = input("What is your name? ")

# Print a friendly greeting where each letter is a different color!
greeting = "Hello, " + name + "! You are a coder now!"

print()
colored = ""
for i in range(len(greeting)):
    color = rainbow[i % len(rainbow)]      # next rainbow color for each letter
    colored = colored + color + greeting[i]
print(BOLD + colored + END)
print()

# A little sparkle animation.
for sparkle in range(3):
    print("        ✨ 🎉 ⭐ 🎉 ✨")
    time.sleep(0.4)

print(GREEN + BOLD + "\nGreat job! 🐢" + END)

# 🔧 TRY THIS:
#   - Change the greeting words.
#   - Add more sparkle lines, or change the emojis.
