# ============================================================
#  MLOLONGO GENERAL HOSPITAL MANAGEMENT SYSTEM
#  Version 1 — with Lists, dictionaries and basics.
#  By: Brevine Oduor Osoro
# ============================================================
import getpass
attempts=0
while attempts <3:
    print( "MLOLONGO GENERAL HOSPITAL MANAGEMENT SYSTEM")
    print( "ADMIN LOG IN ONLY")
    print("ENTER USER NAME AND PASSWORD TO PROCEED")
    user=input("USER NAME:  ")
    password=getpass.getpass("PASSWORD:  ")
    if user== ("OWINOH") and password==("Admin234"):
        print("LOG IN SUCCESSFUL PROCEED TO SESSION")
        patients={ 
    "Gregory Omondi":{"Age": 30, "Ward":"Medical Ward", "Diagnosis":"Malaria", "Gender":"Male"},
    "Tabitha Karanja":{"Age": 67, "Ward":"Medical Ward", "Diagnosis":"Left tibia fructure", "Gender": "Female"},
    "Irene Gidhinji":{ "Age":12, "Ward":"Surgical ward", "Diagnosis":"Tracheostomy", "Gender":"Female"},
    "Hezron Kipngeno":{ "Age":36, "Ward":"Medical Ward", "Diagnosis":"Typhoid with DM1", "Gender": "Male"},
    "James Mosobin":{ "Age":80, "Ward":"Medical Ward", "Diagnosis":"Diabetis Mellitus 2 with HTN", "Gender":"Male"}}
        count=0
        pediatrics=0
        Geriatrics=0
        Adults=0
        for a,b in patients.items():
            print(a)
            for c,d in b.items():
                print(c,d)
            if b["Age"]>0:
             count+=1 
            if b["Age"]<18:
             print("Paediatric")
             pediatrics+=1
            elif b["Age"]<=60:
             print("Adult")
             Adults+=1
            else:
                print("Geriatric")
                Geriatrics+=1
        print( "Total patients is: ", count) 
        print("Geriatrics: " , Geriatrics)
        print("Adults: ", Adults)
        print("Paediatrics: ", pediatrics)
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