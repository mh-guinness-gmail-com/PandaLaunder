"""The providers module exports all providers.
It also includes metadata for each provider to assist usage
"""
from typing import List, Dict
from os.path import dirname, basename, isfile, join
import glob

from src.DAL import DAL
from src.DAL.Provider import Provider as DALProvider
from src.providers.Provider import Provider as ProviderClass


__ending = '.py'

def __get_provider_object(name):
    class_name = f'{str(name).capitalize()}{__ending}'
    class_obj = __import__(class_name, globals(), locals(), [],  1).__dict__[class_name]

    return {
        'name': name,
        'class': class_obj,
        'products': class_obj.products,
    }

def get_providers() -> List[Dict]:
    files = [
        basename(f)[:-len(__ending)]
        for f in glob.glob(join(dirname(__file__), f'*{__ending}'))
        if isfile(f) and not basename(f).startswith('_') and not f.endswith(__file__)
    ]

    return [ __get_provider_object(f) for f in files ]
