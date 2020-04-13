"""The packagers module exports the packagers.
It also exports a factory that creates a packager
"""
from logging import Logger


from .FileSystemPackager import FileSystemPackager
from .InMemoryPackager import InMemoryPackager
from .Packager import Packager


def get_packager(packager_type, *, logger:Logger, output_dir: str, temp_dir: str = '', num_workers:int = 1, **kargs) -> Packager:
    if packager_type == 'm':
        return InMemoryPackager(logger, output_dir)
    elif packager_type == 'f':
        return FileSystemPackager(logger, output_dir, temp_dir, num_workers)
    else:
        raise ValueError('Unknown packager type')
