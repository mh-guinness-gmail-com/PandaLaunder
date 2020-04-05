import json
import urllib.request

import requests

VSCODE_VERSION_LIST_URL = 'https://code.visualstudio.com/sha'
EXTENSION_GALLERY_URL = 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery'

# 0x200 - only latest; 0x2 - include files
EXTENSION_GALLERY_SEARCH_FLAGS = 0x200 + 0x2


def __get_vscode_latest(os_arch: str = 'win32-x64', channel: str = 'stable') -> str:
    response = requests.get(VSCODE_VERSION_LIST_URL)
    versions = json.loads(response.text)['products']
    relevant_versions = [ version for version in versions if version['platform']['os'] == os_arch and version['build'] == channel ]
    return relevant_versions[0]['name']


def __get_extension_metadata(extension_name: str, vscode_version: str) -> dict:
    try:
        headers = {
            'X-Market-Client-Id': vscode_version,
            'content-type': 'application/json',
            'Accept': 'application/json;api-version=3.0-preview.1'
        }
        data = {
            'filters': [{ 'criteria': [{ 'filterType': 7, 'value': extension_name }] }],
            'assetTypes': [ 'Microsoft.VisualStudio.Services.VSIXPackage' ],
            'flags': EXTENSION_GALLERY_SEARCH_FLAGS,
        }
        response = requests.post(EXTENSION_GALLERY_URL, data=json.dumps(data), headers=headers)
        results = json.loads(response.text)['results']
        return results[0]['extensions'][0]['versions'][0]
    except Exception as e:
        raise ValueError(extension_name, vscode_version) from e


def get_extension(extension_name: str, vscode_version: str = __get_vscode_latest()) -> dict:
    metadata = __get_extension_metadata(extension_name, vscode_version)
    version_url = metadata['fallbackAssetUri'] + '/Microsoft.VisualStudio.Services.VSIXPackage'
    return (metadata['version'], version_url)
