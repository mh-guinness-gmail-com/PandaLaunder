import json
import os
import requests
import urllib.request

VSCODE_VERSION_LIST_URL = 'https://code.visualstudio.com/sha'

EXTENSION_GALLERY_ENDPOINT = 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery'
EXTENSION_GALLERY_ENDPOINT_FLAGS = 0x200 + 0x2 # 0x200 - only latest; 0x2 - include files

def __get_vscode_latest(os_arch = 'win32-x64', channel = 'stable'):
    response = requests.get(VSCODE_VERSION_LIST_URL)
    versions = json.loads(response.text)['products']
    relevant_versions = [ version for version in versions if version['platform']['os'] == os_arch and version['build'] == channel ]
    return relevant_versions[0]['name']

def __get_extension_metadata(extension_name, vscode_version):
    try:
        headers = {
            'X-Market-Client-Id': vscode_version,
            'content-type': 'application/json',
            'Accept': 'application/json;api-version=3.0-preview.1'
        }
        data = {
            'filters': [{ 'criteria': [{ 'filterType': 7, 'value': extension_name }] }],
            'assetTypes': [ 'Microsoft.VisualStudio.Services.VSIXPackage' ],
            'flags': EXTENSION_GALLERY_ENDPOINT_FLAGS,
        }
        response = requests.post(EXTENSION_GALLERY_ENDPOINT, data=json.dumps(data), headers=headers)
        results = json.loads(response.text)['results']
        return results[0]['extensions'][0]['versions'][0]
    except Exception as e:
        raise ValueError(extension_name, vscode_version) from e

def __get_vsix_file_path(base_directory, extension_name, extension_version):
    extension_dir = os.path.join(base_directory, extension_name)
    try:
        os.makedirs(extension_dir)
    except:
        pass
    return os.path.join(extension_dir, extension_version + '.vsix')

def get_extension(extension_name, vscode_version = __get_vscode_latest(), base_directory = './extensions'):
    metadata = __get_extension_metadata(extension_name, vscode_version)
    version_url = metadata['fallbackAssetUri'] + '/Microsoft.VisualStudio.Services.VSIXPackage'
    output_path = __get_vsix_file_path(base_directory, extension_name, metadata['version'])
    urllib.request.urlretrieve(version_url, output_path)
