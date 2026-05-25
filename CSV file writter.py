import csv
headers=["Name","Age","Ward","Diagnosis","Gender","DOA"]
file=open("New_patients.csv","w",newline="")
writer=csv.writer(file)
writer.writerow(headers)
file.close()
print("File created with headers successfully")