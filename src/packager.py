import os
from typing import List
from zipfile import ZipFile, ZIP_LZMA
import uuid


def __walk(path: str) -> List[str]:
    ret = []
    if os.path.isfile(path):
        ret = [path]
    elif os.path.exists(path):
        for root, _, files in os.walk(path):
            ret += [os.path.join(root, file) for file in files]
    return ret


def __walkmany(paths: List[str]) -> List[str]:
    return [file for path in paths if path for file in __walk(path)]


def package(paths: List[str], output_base_path: str) -> str:
    os.makedirs(output_base_path, exist_ok=True)
    output_path = '{0}/{1}.zip'.format(output_base_path, uuid.uuid4())
    with ZipFile(output_path, 'w', compression=ZIP_LZMA) as zip_file:
        for file in __walkmany(paths):
            zip_file.write(file)
    return output_path
