# ============================================================
#  MLOLONGO GENERAL HOSPITAL MANAGEMENT SYSTEM
#  Version 4 — with menu
#  By: Brevine Oduor Osoro
# ============================================================

import getpass
import datetime
import csv
import os

# ── FILE SETUP ───────────────────────────────────────────────
def create_file():
    headers = ["Name", "Age", "Ward", "Diagnosis", "Gender", "DOA"]
    if os.path.exists("New_patients.csv"):
        print("File for patients already exists, creation skipped")
    else:
        with open("New_patients.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
        print("File created with headers successfully!")

# ── PATIENT FUNCTIONS ────────────────────────────────────────
def add_patient():
    name      = input("Patient Name: ")
    age       = input("Age: ")
    ward      = input("Ward: ")
    diagnosis = input("Diagnosis: ")
    gender    = input("Gender: ")
    doa       = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with open("New_patients.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, age, ward, diagnosis, gender, doa])
    print("Patient", name, "added successfully")

def read_patients():
    patients = {}
    with open("New_patients.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            patients[row["Name"]] = {
                "Age":       int(row["Age"]),
                "Ward":      row["Ward"],
                "Gender":    row["Gender"],
                "Diagnosis": row["Diagnosis"],
                "DOA":       row["DOA"]
            }
    return patients

def display_patients(patients):
    if not patients:                          # NEW: handle empty file
        print("No patients admitted yet.")
        return
    for name, details in patients.items():
        print("\n" + name)
        for field, value in details.items():
            print(" ", field, ":", value)

def categorize_patients(patients):
    pediatrics = 0
    geriatrics = 0
    adults     = 0
    for name, details in patients.items():
        if details["Age"] < 18:
            print(name, "- Paediatric")
            pediatrics += 1
        elif details["Age"] <= 60:
            print(name, "- Adult")
            adults += 1
        else:
            print(name, "- Geriatric")
            geriatrics += 1
    return pediatrics, adults, geriatrics

def summary(count, paediatrics, adults, geriatrics):
    print("\n---SUMMARY REPORT---")
    print("Total Patients Admitted :", count)
    print("Paediatric patients     :", paediatrics)
    print("Adult patients          :", adults)
    print("Geriatric patients      :", geriatrics)

# ── LOGIN ────────────────────────────────────────────────────
def login():
    user     = input("USERNAME: ")
    password = getpass.getpass("PASSWORD: ")
    if user == "OWINOH" and password == "Admin234":
        return True
    return False

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

        input("\nPress Enter to continue...")  # pause before showing menu again

# ── PROGRAM START ────────────────────────────────────────────
if __name__ == "__main__":
    create_file()                            # create CSV if it doesn't exist
    NOW = datetime.datetime.now()
    attempts = 0

    while attempts < 3:                      # login loop — max 3 attempts
        print("\n" + "="*40)
        print("  MLOLONGO GENERAL HOSPITAL")
        print("  ADMIN LOGIN ONLY")
        print("="*40)

        if login():
            print("\nLogin successful! Welcome.")
            print("Session started:", NOW.strftime("%d/%m/%Y %H:%M"))
            run_menu()                       # ← hand over to the menu
            break                            # after menu exits, stop login loop

        else:
            attempts += 1
            remaining = 3 - attempts
            if attempts == 3:
                print("\n⚠ WRONG DETAILS!")
                print("Attempts exceeded. System locked. Please contact admin.")
            else:
                print("\nWrong details. Try again.")
                print("Attempts remaining:", remaining)