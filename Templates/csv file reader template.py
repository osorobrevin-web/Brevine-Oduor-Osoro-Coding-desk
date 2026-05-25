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