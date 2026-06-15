# The Magic Doors! 🚪✨
# This is a choose-your-own-adventure. The program asks you a question and then
# does something DIFFERENT depending on your answer. That's called an "if".

import time

CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
PURPLE = "\033[95m"
BOLD   = "\033[1m"
END    = "\033[0m"

def say(text, color=CYAN):
    print(color + BOLD + text + END)
    time.sleep(0.6)

say("\n🏰 You are standing in a magic castle.")
say("There are two doors: a RED door and a BLUE door.")

# Ask the player to choose. We make the answer lowercase so "RED", "Red"
# and "red" all work the same.
choice = input("Which door do you open? Type red or blue: ").strip().lower()

# "if" checks the answer and picks what happens next.
if choice == "red":
    say("\n🔴 You open the red door...", YELLOW)
    say("A friendly dragon gives you a high five! 🐉🙌", GREEN)
elif choice == "blue":
    say("\n🔵 You open the blue door...", CYAN)
    say("You find a pool full of rubber ducks! 🦆🦆🦆", GREEN)
else:
    # This runs if the answer was not red or blue.
    say("\n🤔 That's not red or blue... so a silly goose appears!", PURPLE)
    say("HONK! 🪿  (Run it again and pick red or blue!)", GREEN)

say("\n✨ The End. Want to play again? Run it once more!\n", PURPLE)

# 🔧 TRY THIS:
#   - Change what's behind each door.
#   - Add a third door! Add a GREEN door with another `elif`.
