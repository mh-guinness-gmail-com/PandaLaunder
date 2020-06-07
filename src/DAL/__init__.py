"""The providers module exports all databases.
"""
from typing import List, Dict


from src.import_util import import_all_public_sibling_modules


default = 'fs'

def get_databases() -> List[Dict]:
    return [
        {
            'name': class_obj[name].name,
            'class': class_obj[name],
        }
        for name, class_obj in import_all_public_sibling_modules(__file__).items()
    ]
