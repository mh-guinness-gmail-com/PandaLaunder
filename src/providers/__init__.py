from .Npm import Npm
from .Vscode import Vscode
from .Provider import Provider
from .. import Product


providers = [
    {
        'name': 'npm',
        'products': 'npm packages',
        'class': Npm,
    },
    {
        'name': 'vscode',
        'products': 'vscode extensions',
        'class': Vscode,
    },
]