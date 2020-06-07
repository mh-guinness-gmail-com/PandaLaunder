from typing import List, Dict, Tuple
import os
import importlib.util


__ending = '.py'

def __import_module(module_name: str, module_path: str) -> Dict:
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
        return (name, __import_module(name, path))
    except:
        return None

def import_all_public_sibling_modules(module_path: str) -> List[Dict[str, Dict]]:
    module_path = os.path.normpath(module_path)

    siblings = [ __import_sibling(path, [ module_path ]) for path in os.listdir(os.path.dirname(module_path))]

    return { name: module for name, module in siblings if module }
