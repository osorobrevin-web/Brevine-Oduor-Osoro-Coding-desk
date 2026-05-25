import csv
file=(open("Mlolongo hospital data.csv","r"))
reader=csv.DictReader(file)
for row in reader:
    print({row["Name"]}|"Age",row["Age"],"Diagnosis",row["Diagnosis"],"Ward",row["Ward"],"Gender",row["gender"],"Date of Admission",row["DOA "])
file.close()   

file=open("New_patients.csv","w",newline="")
writer=csv.writer(file)
writer.writerow(headers)
file.close()
print("File created with headers successfully")