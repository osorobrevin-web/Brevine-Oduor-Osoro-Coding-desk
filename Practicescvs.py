import csv
file=(open("Mlolongo hospital data.csv","r"))
reader=csv.DictReader(file)
for row in reader:
    print({row["Name"]}|"Age",row["Age"],"Diagnosis",row["Diagnosis"],"Ward",row["Ward"],"Gender",row["gender"],"Date of Admission",row["DOA "])
file.close()   