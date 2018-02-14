import csv, sys


file_name = sys.argv[1]

lines = []
print(file_name)

with open(file_name, newline='') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        lines.append(row)

print(lines[0])
