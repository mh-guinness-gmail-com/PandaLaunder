"""The providers module exports all providers.
It also includes metadata for each provider to assist usage
"""

from ..DAL.db import get_providers

def get_providers_classes():
    providers = get_providers()
    
    for provider in providers:
        class_name = '{0}'.format(str(provider['name']).capitalize())
        provider['class'] = __import__(class_name, globals(), locals(), [],  1).__dict__[class_name]
    return providers
