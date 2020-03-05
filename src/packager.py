import os
from typing import List
from zipfile import ZipFile, ZIP_LZMA


def __walk(path: str) -> List[str]:
    ret = []
    if os.path.isfile(path):
        ret = [path]
    elif os.path.exists(path):
        for root, _, files in os.walk(path):
            ret += [os.path.join(root, file) for file in files]
    return ret


def __walkmany(paths: List[str]):
    return [file for path in paths if path for file in __walk(path)]


def package(paths: List[str], output_path: str = 'output.zip') -> None:
    with ZipFile(output_path, 'w', compression=ZIP_LZMA) as zip:
        for file in __walkmany(paths):
            zip.write(file)
