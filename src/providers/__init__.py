from .Npm import Npm
from .Vscode import Vscode

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
