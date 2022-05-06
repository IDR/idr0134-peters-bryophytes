
import csv

rows = []

base_dir = "/uod/idr/filesets/idr0134-peters-bryophytes/20211214-Globus/"

# with open("experimentA/idr0134-experimentA-filePaths.tsv") as file:
with open("experimentA/idr0134-experimentA-filePaths.tsv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        line = row[0]
        print("line", line)
        path = line.replace(base_dir, "")
        ds_name = path.split("/")[0]
        rows.append(["Dataset:name:" + ds_name, line])

# write tsv
with open('idr0134-experimentA-filePaths2.tsv', 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for row in rows:
        writer.writerow(row)
