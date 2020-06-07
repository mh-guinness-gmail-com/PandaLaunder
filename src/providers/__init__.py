"""The providers module exports all providers.
It also includes metadata for each provider to assist usage
"""
from typing import List, Dict

from src.import_util import import_all_public_sibling_modules

def get_providers() -> List[Dict]:
    return [
        {
            'name': class_obj[name].name,
            'class': class_obj[name],
            'products': class_obj[name].products,
        }
        for name, class_obj in import_all_public_sibling_modules(__file__).items()
    ]
