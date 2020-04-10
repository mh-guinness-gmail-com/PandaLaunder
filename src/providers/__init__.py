from .Npm import Npm as __npm
from .Vscode import Vscode as __vscode

providers = [
    {
        'name': 'npm',
        'products': 'npm packages',
        'class': __npm,
    },
    {
        'name': 'vscode',
        'products': 'vscode extensions',
        'class': __vscode,
    },
]
