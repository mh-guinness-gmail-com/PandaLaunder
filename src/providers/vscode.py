import json
import requests
import urllib.request
import ssl

from src.providers.Provider import Provider

VSCODE_VERSION_LIST_URL = 'https://code.visualstudio.com/sha'
EXTENSION_GALLERY_URL = 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery'
# 0x200 - only latest; 0x2 - include files
EXTENSION_GALLERY_SEARCH_FLAGS = 0x200 + 0x2
ssl._create_default_https_context = ssl._create_unverified_context


class Vscode(Provider):
    def __init__(self):
        Provider.__init__(self)

    def provide(self, products):
        vscode_version = self.__get_vscode_latest()
        extensions = [(self._get_extension(extention, vscode_version), extention) for extention in products]
        return ([(extention, version, url) for (version, url), extention in extensions], 'vsix', 'vscode')

    def __get_vscode_latest(self, os_arch: str = 'win32-x64', channel: str = 'stable') -> str:
        response = requests.get(VSCODE_VERSION_LIST_URL)
        versions = json.loads(response.text)['products']
        relevant_versions = [ version for version in versions if version['platform']['os'] == os_arch and version['build'] == channel ]
        return relevant_versions[0]['name']

    def __get_extension_metadata(self, extension_name: str, vscode_version: str) -> dict:
        try:
            headers = {
                'X-Market-Client-Id': vscode_version,
                'content-type': 'application/json',
                'Accept': 'application/json;api-version=3.0-preview.1'
            }
            data = {
                'filters': [{ 'criteria': [{ 'filterType': 7, 'value': extension_name }]}],
                'assetTypes': [ 'Microsoft.VisualStudio.Services.VSIXPackage' ],
                'flags': EXTENSION_GALLERY_SEARCH_FLAGS,
            }
            response = requests.post(EXTENSION_GALLERY_URL, data=json.dumps(data), headers=headers)
            results = json.loads(response.text)['results']
            return results[0]['extensions'][0]['versions'][0]
        except Exception as e:
            raise ValueError(extension_name, vscode_version) from e

    def _get_extension(self, extension_name: str, vscode_version: str) -> dict:
        metadata = self.__get_extension_metadata(extension_name, vscode_version)
        version_url = metadata['fallbackAssetUri'] + '/Microsoft.VisualStudio.Services.VSIXPackage'
        return (metadata['version'], version_url)
