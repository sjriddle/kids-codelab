# Counting rocket! 🚀
# Let's count DOWN from 5, then blast off! A loop counts for us,
# and time.sleep makes the computer wait one second between numbers.

import time

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
END = "\033[0m"

print(CYAN + BOLD + "\n   Get ready to launch! 🚀\n" + END)
time.sleep(1)

# Count down: 5, 4, 3, 2, 1
for number in [5, 4, 3, 2, 1]:
    print(YELLOW + BOLD + "        " + str(number) + " ..." + END)
    time.sleep(1)  # wait one second

print(RED + BOLD + "\n        BLAST OFF!\n" + END)
time.sleep(0.5)

# Make the rocket fly UP the screen.
sky_height = 10
for step in range(sky_height):
    # Print blank lines to push the rocket higher each time.
    blank_lines = sky_height - step
    print("\n" * blank_lines + "          🚀")
    time.sleep(0.2)

print(GREEN + BOLD + "\n   🌟 The rocket reached the stars! 🌟\n" + END)

# 🔧 TRY THIS:
#   - Count down from 10 instead: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1].
#   - Make the rocket fly slower: change 0.2 to 0.5.
#   - Change the 🚀 to a different emoji, like 🦅 or ✈️.
