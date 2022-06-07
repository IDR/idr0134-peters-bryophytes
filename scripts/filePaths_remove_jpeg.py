
import csv

# This script removes all .tiff and .jpeg filePaths IF there is a
# corresponding .ome.tiff file in the same dir

imagePaths = set()

# Read all image paths...
with open("allFiles.txt") as inputFile:
    imagePaths = set([line.strip() for line in inputFile.readlines()])

print("Read filenames", len(imagePaths))

GLOBUS_DIR = "20211214-Globus"
FTP_DIR = "20220531-ftp"

# read again, removing .tiff and .jpeg ONLY if .ome.tiff exists
with open("allFiles.txt") as inputFile:
    with open('noJpegTiffDuplicates7thJune.txt', 'w') as outFile:
        for imgPath in inputFile.readlines():
            imgPath = imgPath.strip()
            # remove hidden files
            if "/." in imgPath:
                continue
            # remove .jpeg if corresponding .tiff or .ome.tiff is found
            if imgPath.endswith(".jpeg"):
                ome_path = imgPath.replace(".jpeg", ".ome.tiff")
                tiff_path = imgPath.replace(".jpeg", ".tiff")
                if ome_path in imagePaths or tiff_path in imagePaths:
                    continue
                # Also check in later ftp dir...
                if tiff_path.replace(GLOBUS_DIR, FTP_DIR) in imagePaths or ome_path.replace(GLOBUS_DIR, FTP_DIR) in imagePaths:
                    continue
                
            if imgPath.endswith(".tiff") and not imgPath.endswith(".ome.tiff"):
                tiff_path = imgPath.replace(".tiff", ".ome.tiff")
                if tiff_path in imagePaths or tiff_path.replace(GLOBUS_DIR, FTP_DIR) in imagePaths:
                    continue
            
            if imgPath.endswith(".TIF") and not imgPath.endswith(".ome.tiff"):
                tiff_path = imgPath.replace(".TIF", ".ome.tiff")
                if tiff_path in imagePaths or tiff_path.replace(GLOBUS_DIR, FTP_DIR) in imagePaths:
                    continue
            outFile.write(imgPath + "\n")
