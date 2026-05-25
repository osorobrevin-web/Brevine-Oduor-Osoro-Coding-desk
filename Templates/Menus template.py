# ── MENU ─────────────────────────────────────────────────────
# NEW: shows the menu options — just printing, nothing else
def show_menu():
    print("\n" + "="*40)
    print("   MLOLONGO GENERAL HOSPITAL SYSTEM")
    print("="*40)
    print("  1. View all patients")
    print("  2. Add new patient")
    print("  3. Categorize patients by age")
    print("  4. Summary report")
    print("  5. Exit")
    print("="*40)

# NEW: the menu loop — runs after successful login
def run_menu():
    while True:                              # keep showing menu until Exit
        show_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            patients = read_patients()       # re-read so new patients show up
            display_patients(patients)

        elif choice == "2":
            add_patient()

        elif choice == "3":
            patients = read_patients()
            categorize_patients(patients)

        elif choice == "4":
            patients = read_patients()
            p, a, g  = categorize_patients(patients)
            count    = len(patients)
            summary(count, p, a, g)

        elif choice == "5":
            print("\nSession ended. Goodbye! 👋")
            break                            # EXIT the menu loop

        else:
            print("\n⚠ Invalid choice. Enter a number between 1 and 5.")

        input("\nPress Enter to continue...")