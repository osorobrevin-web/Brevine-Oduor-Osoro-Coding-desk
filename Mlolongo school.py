# ============================================================
#  MLOLONGO STUDENT MANAGEMEMT SYSTEM
#  Version 1 — with while loop, nested dictinary and log in
#  By: Brevine Oduor Osoro
# ============================================================
while True:
    print("MLOLONGO STUDENT MANAGEMEMT SYSTEM")
    students= ("Jane Omondi","Ephy Akoth","Stacy Otieno", "Odhiambo Kevin","Melvin Oduor")
    Age=("19","16","20","17","22")
    MAT=("78","45","88","32","65")
    ENG=("82","50","93","28","78")
    SCI= ("75", "48", "85", "35", "68")
    user= input("User Name: ")
    password= input("Password: ")
    if user== "admin" and password== "1234":
        print("LOG IN SUCCESSFUL")
        for i in range (5):
            T= int(MAT[i])+ int(ENG[i])+int(SCI[i])
            Average= round(T/3, 2)
            if Average >=80:
                print(students[i], "Age", Age[i], "Mathematics", MAT[i], "English", ENG[i], "Science", SCI[i],"Total marks",T, "Average",Average,"Mean Grade A pass ")
            elif Average>=70:
                print(students[i], "Age", Age[i], "Mathematics", MAT[i], "English", ENG[i], "Science", SCI[i],"Total marks",T,"Average", Average,"Mean Grade B Pass ")
            elif Average >= 60:
                print(students[i], "Age", Age[i], "Mathematics", MAT[i], "English", ENG[i], "Science", SCI[i],"Total marks",T, "Average",Average,"Mean Grade C pass")
            elif Average>=50:
             print(students[i], "Age", Age[i], "Mathematics", MAT[i], "English", ENG[i], "Science", SCI[i],"Total marks",T,"Average",Average,"Mean Grade D Pass")
            else:
                 print(students[i], "Age", Age[i], "Mathematics", MAT[i], "English", ENG[i], "Science", SCI[i],"Total marks",T, "Average", Average, "Mean Grade E Fail")         
        break   
    else:
        print("WRONG DETAILS ACCESS DENIED")