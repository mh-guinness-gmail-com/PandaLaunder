"""The providers module exports all databases.
"""
from typing import List, Dict


from src.import_util import import_all_public_sibling_modules


default = 'fs'

def get_databases() -> List[Dict]:
    return import_all_public_sibling_modules(__file__)
