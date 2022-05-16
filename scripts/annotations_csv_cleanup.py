
import csv

# This script renames images in annotations.csv from .ome to .ome.tiff.
# It also removes unused rows from annotations.csv (where the image is
# not found in filePaths.tsv).

imagePaths = set()

data_dir = "/uod/idr/filesets/idr0134-peters-bryophytes/20211214-Globus/"

# Read all image paths in filePaths...
with open("experimentA/idr0134-experimentA-filePaths.tsv") as inputFile:
    reader = csv.reader(inputFile, delimiter='\t')
    for row in reader:
        imgPath = row[1]
        imgPath = imgPath.replace(data_dir, "")
        # print("imgPath", imgPath)
        imagePaths.add(imgPath)
# print("Read filenames", len(imagePaths))

renamed_images = []
annotations_without_filepath = []

# read again, removing .tiff and .jpeg ONLY if .ome.tiff exists
with open("experimentA/idr0134-scapaniaceae-annotation.csv") as inputFile:
    with open('idr0134-scapaniaceae-annotation2.csv', 'w') as outFile:
        reader = csv.reader(inputFile, delimiter=',')
        writer = csv.writer(outFile, delimiter=',')
        image_column = None
        dataset_column = None
        for row in reader:
            if image_column is None:
                image_column = row.index("Image File")
                dataset_column = row.index("Dataset Name")
                writer.writerow(row)
                continue
            image_name = row[image_column]
            dataset_name = row[dataset_column]
            image_path = f"{dataset_name}/{image_name}"
            if image_path in imagePaths:
                # exact match
                writer.writerow(row)
                imagePaths.remove(image_path)
                continue
            renamed = image_path.replace(".tiff", ".ome.tiff")
            if renamed in imagePaths:
                # rename .tiff to .ome.tiff
                row[image_column] = image_name.replace(".tiff", ".ome.tiff")
                writer.writerow(row)
                imagePaths.remove(renamed)
                renamed_images.append(renamed)
                continue
            renamed = image_path + ".TIF"
            if renamed in imagePaths:
                # rename image to image.TIF
                row[image_column] = image_name + ".TIF"
                writer.writerow(row)
                imagePaths.remove(renamed)
                renamed_images.append(renamed)
                continue
            # print("NOT found", image_path)
            annotations_without_filepath.append(image_path)


print("annotations_without_filepath", len(annotations_without_filepath))
with open('annotations_without_filepath.csv', 'w') as outFile:
    writer = csv.writer(outFile, delimiter=',')
    for row in annotations_without_filepath:
        writer.writerow([row])


print("IMAGE PATHS with no annotations", len(imagePaths))

with open('filePaths_no_annotations.csv', 'w') as outFile:
    writer = csv.writer(outFile, delimiter=',')
    for row in imagePaths:
        writer.writerow([row])

# print("renamed_images", renamed_images)
print("renamed_images", len(renamed_images))
