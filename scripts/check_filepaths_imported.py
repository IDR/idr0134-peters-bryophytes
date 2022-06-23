from omero.gateway import BlitzGateway
from omero.cli import cli_login
import argparse
import csv

DESC = '''
Checks an IDR Project against filePaths.tsv to see if any images failed import
'''

parser = argparse.ArgumentParser(description=DESC)
parser.add_argument("target", help="Project:123 or Screen:123")
parser.add_argument("file", nargs="?", help="The filePaths.tsv file")

args = parser.parse_args()

target = args.target.split(':')
if target[0] == 'Project':
    projectId = int(target[1])

ds_keys = set()

# read tsv
with open(args.file, 'r') as tsv_in:
    reader = csv.reader(tsv_in, delimiter='\t')
    for row in reader:
        project_dataset = row[0]
        dataset = project_dataset.split("Dataset:name:")[1]
        image = row[2]
        key = "{},{}".format(dataset, image)
        ds_keys.add(key)

with cli_login() as cli:
    conn = BlitzGateway(client_obj=cli._client)
    project = conn.getObject("Project", projectId)
    for ds in sorted(project.listChildren(), key=lambda x: x.getName()):
        for img in sorted(ds.listChildren(), key=lambda x: x.getName()):
            key = "{},{}".format(ds.getName(), img.getName())
            if key not in ds_keys:
                print(key, "Not found in filePaths.tsv")
            else:
                ds_keys.remove(key)

for key in ds_keys:
    print("NOT imported", key)
