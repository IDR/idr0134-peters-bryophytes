
import csv
from ftplib import ftpcp

rows = []

base_dir = "/uod/idr/filesets/idr0134-peters-bryophytes/"
globas_dir = "20211214-Globus/"
ftp_dir = "20220531-ftp/"
project = "Project:name:idr0134-peters-bryophytes/experimentA/"

# 3 files were re-uploaded (ftp failed), but the other 2 were already in Globus upload
reuploaded_img = "IMG_9021 Scapania aequiloba stature dorsal side (MP-E 2x).ome.tiff"
reuploaded_dir = "20220608-ftp/"

img_keys = set()
duplicates = 0
with open("noJpegTiffDuplicates7thJune.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        line = row[0]
        if not ".ome.tiff" in line:
            continue
        path = line.replace(base_dir, "").replace(globas_dir, "").replace(ftp_dir, "")
        # Fix "spitzbergensis" -> "spitsbergensis"
        ds_name = path.split("/")[0].replace("spitzbergensis", "spitsbergensis")
        img_name = path.split("/")[-1].replace("spitzbergensis", "spitsbergensis")
        img_key = f'{ds_name},{img_name}'
        if img_name == reuploaded_img:
            line = line.replace(ftp_dir, reuploaded_dir)
        if img_key not in img_keys:
            rows.append([project + "Dataset:name:" + ds_name, line, img_name])
            img_keys.add(img_key)
        else:
            print("Duplicate", line)
            duplicates += 1

print("Duplicates: ", duplicates)

# write tsv
with open('idr0134-experimentA-filePaths.tsv', 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for row in rows:
        writer.writerow(row)
