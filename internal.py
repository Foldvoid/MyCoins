import zipfile
import os
import shutil

import slang

zip_filename = "internal.zip"
extract_dir = os.path.splitext(zip_filename)[0]

def get_internal():
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    file_path = os.path.join(extract_dir, "gecko.txt")

    with open(file_path, 'r') as f:
        first_line = f.readline().strip()

    first_line = slang.jaber(first_line)

    shutil.rmtree(extract_dir)
    return first_line