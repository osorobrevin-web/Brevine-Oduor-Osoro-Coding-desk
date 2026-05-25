import csv
import os
headers=["Name","Age","Ward","Diagnosis","Gender","DOA"]
if os.path.exists("New_patients.csv"):
    print("File for patients already exists, creation skipped")
else:
    file=open("New_patients.csv","w",newline="")
    writer=csv.writer(file)
    writer.writerow(headers)
    file.close()
    print("File created with headers successfully!")
