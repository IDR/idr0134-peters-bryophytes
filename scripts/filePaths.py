
import csv

rows = []

base_dir = "/uod/idr/filesets/idr0134-peters-bryophytes/"
globas_dir = "20211214-Globus/"
ftp_dir = "20220531-ftp/"
project = "Project:name:idr0134-peters-bryophytes/experimentA/"

# 5 more uploaded "20220624-ftp" - NB: see below...
ftp_20220624 = [
    "IMG_9021 Scapania aequiloba stature dorsal side (MP-E 2x).ome.tiff",
    "IMG_3568-3667 Diplophyllum taxifolium antical lobe basal leaf margin (40x).ome.tiff",
    "IMG_3368-3467 Diplophyllum taxifolium postical lobe leaf base (40x).ome.tiff",
    "IMG_3245-3344 Diplophyllum taxifolium postical lobe leaf center (40x).ome.tiff",
    "IMG_2497-2596 Douinia ovata postical lobe leaf center (40x).ome.tiff"
]

typos = [
    ["frisch", "fresh"],
    ["spitzbergensis", "spitsbergensis"],
    ["scapania_ hyperborea", "scapania_hyperborea"],
    ["stature_oberunterseite", "stature_dorsal_and_ventral_sides"]
]
def fix_typos(text):
    for typo in typos:
        text = text.replace(typo[0], typo[1])
    return text

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
        ds_name = fix_typos(path.split("/")[0])
        img_name = fix_typos(path.split("/")[-1])
        img_key = f'{ds_name},{img_name}'
        if img_name in ftp_20220624:
            line = line.replace(globas_dir, "20220624-ftp")
            line = line.replace(ftp_dir, "20220624-ftp")
            # NB: these lines needed manual editing after this, to remove /dir in  "20220624-ftp/dir"
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
