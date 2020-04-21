"""The packagers module exports the packagers.
It also exports a factory that creates a packager
"""
from logging import Logger


from .FileSystemPackager import FileSystemPackager
from .InMemoryPackager import InMemoryPackager
from .Packager import Packager

packager_type_codes = {
    'm': InMemoryPackager,
    'f': FileSystemPackager,
}

default_packager_type_code = 'm'

def get_packager(packager_type_code, *, logger:Logger, output_dir: str, temp_dir: str = '', num_workers:int = 1, **kargs) -> Packager:
    packager = packager_type_codes[packager_type_code]
    if packager == InMemoryPackager:
        return InMemoryPackager(logger, output_dir)
    elif packager == FileSystemPackager:
        return FileSystemPackager(logger, output_dir, temp_dir, num_workers)
    else:
        raise ValueError('Unknown packager type')
