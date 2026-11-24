import csv

with open("../reports/practice.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["Test ID", "Voltage", "Result"])

    writer.writerow(["TC-001", 3.333333, "PASS"])

print("CSV report created successfully!")

