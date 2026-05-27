# ============================================================
#  MLOLONGO GENERAL HOSPITAL MANAGEMENT SYSTEM
#  Version 2 — with functions and csv data file reading
#  By: Brevine Oduor Osoro
# ============================================================
import getpass
import datetime
import csv
def read_patients():
    patients={}
    file=open("Mlolongo General Hospital data.csv","r")
    reader=csv.DictReader(file)
    for row in reader:
        patients[row["Name"]]={
            "Age":int(row["Age"]),
            "Ward":row["Ward"],
            "Gender":row["gender"],
            "Diagnosis":row["Diagnosis"],
            "DOA":row["DOA"] 
        }
            
    file.close()
    return patients
    
def login():
    user=input("USER NAME:  ")
    password=getpass.getpass("PASSWORD:  ")
    if user== ("OWINOH") and password==("Admin234"):
        return True
    return False
def display_patients(patients):
    for a,b in patients.items():
            print(a)
            for c,d in b.items():
                print(c,d)
def categorize_patients(patients):
    pediatrics=0
    Geriatrics=0
    Adults=0
    for a,b in patients.items(): 
            if b["Age"]<18:
                print(a,"Paediatric")
                pediatrics+=1
            elif b["Age"]<=60:
                print( a, "Adult")
                Adults+=1
            else:
                print( a,"Geriatric")
                Geriatrics+=1 
    return pediatrics, Adults, Geriatrics 
def summary(count,paediatrics,adults,geriatrics):
    print("---SUMARY REPORT---")
    print("Total Patients Anitted",count)
    print("Paediatrics patients",paediatrics)
    print("Geriatics patients",geriatrics)
    print("Adults patients",adults)

attempts=0
patients=read_patients()
NOW= datetime.datetime.now()
while attempts <3:
    print( "MLOLONGO GENERAL HOSPITAL MANAGEMENT SYSTEM")
    print( "ADMIN LOG IN ONLY")
    print("ENTER USER NAME AND PASSWORD TO PROCEED")
    if login():
        print("LOG IN SUCCESSFUL PROCEED TO SESSION")
        print("ADMITTED PATIENTS AS AT",NOW.strftime( " %d/%m/%Y, %H:%m"))
        display_patients(patients)
        p,a,g= categorize_patients(patients)
        count=len(patients)
        summary(count,p,a,g)
        break
    else:
        attempts+=1
        remaining=3- attempts
        if attempts ==3:
            print("WRONG DETAILS !!!")
            print(" Number of availlable attempts exceeded . System Locked please contact admin")
        else:
            print("WRONG DETAILS PLEASE TRY AGAIN")
            print("number of attempts remainig is ", remaining,"until system locks")