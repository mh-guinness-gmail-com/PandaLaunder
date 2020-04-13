"""The providers module exports all providers.
It also includes metadata for each provider to assist usage
"""
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
