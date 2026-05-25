import csv
import datetime
name=input("Patient Name: ")
age=input("Age: ")
ward=input("Ward: ")
diagnosis=input("Diagnosis: ")
gender=input("Gender: ")
doa=datetime.datetime.now().strftime("%d/%m/%y %H:%M")
file=open("New_patients.csv","a",newline="")
writer=csv.writer(file)
writer.writerow([name,age,ward,diagnosis,gender,doa])
file.close()
print("Patient",name,"added successfully")