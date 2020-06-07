"""The providers module exports all providers.
It also includes metadata for each provider to assist usage
"""
from typing import List, Dict


from src.import_util import import_all_public_sibling_modules

from ._Provider import Provider

def get_providers() -> List[Dict]:
    return import_all_public_sibling_modules(__file__)
