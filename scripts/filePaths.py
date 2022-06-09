
import csv
from ftplib import ftpcp

rows = []

base_dir = "/uod/idr/filesets/idr0134-peters-bryophytes/"
globas_dir = "20211214-Globus/"
ftp_dir = "20220531-ftp/"
project = "Project:name:idr0134-peters-bryophytes/experimentA/"

with open("noJpegTiffDuplicates7thJune.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        line = row[0]
        print("line", line)
        if not ".ome.tiff" in line:
            continue
        path = line.replace(base_dir, "").replace(globas_dir, "").replace(ftp_dir, "")
        # Fix "spitzbergensis" -> "spitsbergensis"
        ds_name = path.split("/")[0].replace("spitzbergensis", "spitsbergensis")
        img_name = path.split("/")[-1].replace("spitzbergensis", "spitsbergensis")
        rows.append([project + "Dataset:name:" + ds_name, line, img_name])

# write tsv
with open('idr0134-experimentA-filePaths.tsv', 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for row in rows:
        writer.writerow(row)
