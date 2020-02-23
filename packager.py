import os
from zipfile import ZipFile, ZIP_LZMA

def package(directoy: str, output_path: str = 'output.zip') -> None:
    with ZipFile(output_path, 'w', compression=ZIP_LZMA) as zip:
        for root, _, files in os.walk(directoy):
            for file in files:
                output_path = os.path.join(root, file)
                zip.write(output_path)
