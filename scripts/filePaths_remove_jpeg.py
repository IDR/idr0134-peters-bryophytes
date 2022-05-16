
import csv

# This script removes all .tiff and .jpeg filePaths IF there is a
# corresponding .ome.tiff file in the same dir

imagePaths = set()

# Read all image paths...
with open("experimentA/idr0134-experimentA-filePaths.tsv") as inputFile:
    reader = csv.reader(inputFile, delimiter='\t')
    for row in reader:
        imgPath = row[1]
        imagePaths.add(imgPath)
print("Read filenames", len(imagePaths))

# read again, removing .tiff and .jpeg ONLY if .ome.tiff exists
with open("experimentA/idr0134-experimentA-filePaths.tsv") as inputFile:
    with open('idr0134-experimentA-filePaths2.tsv', 'w') as tsvfile:
        reader = csv.reader(inputFile, delimiter='\t')
        writer = csv.writer(tsvfile, delimiter='\t')
        for row in reader:
            imgPath = row[1]
            ignore = False
            for ext in [".jpeg", ".tiff"]:
                if imgPath.endswith(ext) and not imgPath.endswith(".ome.tiff"):
                    print("imgPath", imgPath)
                    if imgPath.replace(ext, ".ome.tiff") in imagePaths:
                        # can ignore
                        print("IGNORE -------")
                        ignore = True
            if not ignore:    
                # write
                writer.writerow(row)
