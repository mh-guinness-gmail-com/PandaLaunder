from typing import List, Dict, Tuple
import os
import importlib.util


__ending = '.py'

def __calc_module_name(module_path: str) -> str:
    module_path = os.path.relpath(module_path, __file__)
    parts = __name__.split('.')
    for part in module_path.split(os.path.sep):
        if '.' in part and module_path.endswith(part):
            part = '.'.join(part.split('.')[:-1])
        if part == '.':
            continue
        elif part == '..':
            parts.pop()
        else:
            parts.append(part)
    return '.'.join(parts)

def __import_module(module_path: str) -> Dict:
    module_name = __calc_module_name(module_path)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def __import_sibling(path: str, exclude: List[str]) -> Tuple[str, Dict]:
    try:
        path = os.path.normpath(path)
        if path in exclude:
            return None
        name, _ = os.path.splitext(os.path.basename(path))
        if name.startswith('_'):
            return None
        return (name, __import_module(path))
    except:
        return None

def import_all_public_sibling_modules(module_path: str) -> List[Dict[str, Dict]]:
    module_path = os.path.normpath(module_path)
    dir_path = os.path.dirname(module_path)

    siblings = [ __import_sibling(os.path.join(dir_path, path), [ module_path ]) for path in os.listdir(os.path.dirname(module_path))]

    live_siblings = [ sibling for sibling in siblings if sibling ]

    return [ module.__dict__[name] for name, module in live_siblings ]
