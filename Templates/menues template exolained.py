 ============================================================
#  PYTHON MENU TEMPLATE
#  By: Brevine Oduor Osoro
#  Reference file — copy and adapt for any project
# ============================================================
 
# ── STEP 1: IMPORT what you need ────────────────────────────
# Add your imports at the top of every Python file
import datetime   # example import — remove if not needed
 
 
# ── STEP 2: DEFINE your action functions ────────────────────
# Each option in the menu gets its own function.
# One function = one job. This is the golden rule.
 
def option_one():
    """Describe what option one does here."""
    print("\n--- Option One ---")
    # your code goes here
    input("\nPress Enter to return to menu...")   # pauses before going back
 
def option_two():
    """Describe what option two does here."""
    print("\n--- Option Two ---")
    # your code goes here
    input("\nPress Enter to return to menu...")
 
def option_three():
    """Describe what option three does here."""
    print("\n--- Option Three ---")
    # your code goes here
    input("\nPress Enter to return to menu...")
 
 
# ── STEP 3: DISPLAY the menu ────────────────────────────────
# This function only prints the menu — nothing else.
# Keeping display separate from logic is good structure.
 
def show_menu():
    print("\n" + "="*40)
    print("   YOUR PROGRAM TITLE HERE")
    print("="*40)
    print("  1. Option One")
    print("  2. Option Two")
    print("  3. Option Three")
    print("  4. Exit")
    print("="*40)
 
 
# ── STEP 4: THE MENU LOOP ───────────────────────────────────
# This is the engine of the menu.
# It keeps running until the user chooses to exit.
#
# HOW IT WORKS:
#   while True        → loop forever
#   show_menu()       → display the options
#   input()           → wait for user to type a choice
#   if/elif/else      → decide what to do based on choice
#   break             → exit the loop (and the program)
 
def main():
    while True:                          # keep looping until 'break'
        show_menu()                      # show the options
        choice = input("Enter choice (1-4): ").strip()  # .strip() removes accidental spaces
 
        if choice == "1":
            option_one()
        elif choice == "2":
            option_two()
        elif choice == "3":
            option_three()
        elif choice == "4":
            print("\nGoodbye! 👋")
            break                        # EXIT the while loop → program ends
        else:
            print("\n⚠ Invalid choice. Please enter a number between 1 and 4.")
            # no break → loop continues, menu shows again
 
 
# ── STEP 5: RUN the program ─────────────────────────────────
# This line means: "only run main() if THIS file is run directly"
# If another file imports this one, main() will NOT run automatically.
# Always put this at the bottom of your file.
 
if __name__ == "__main__":
    main()
 
 
# ============================================================
#  QUICK REFERENCE — Menu building blocks
# ============================================================
#
#  while True:           → infinite loop
#  break                 → exit the loop
#  continue              → skip to next loop cycle
#  .strip()              → remove spaces from user input
#  input("...").strip()  → safest way to get user input
#
#  MENU STRUCTURE:
#  ┌─────────────────────────────┐
#  │  show_menu()  ← just prints │
#  │  main()       ← the loop    │
#  │  option_x()   ← the actions │
#  └─────────────────────────────┘
#
#  TO ADD A NEW OPTION:
#  1. Define a new function: def option_four(): ...
#  2. Add it to show_menu(): print("  4. Option Four")
#  3. Add it to main():      elif choice == "4": option_four()
#  That's it!
# ============================================================