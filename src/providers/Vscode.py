import requests
import json


from .Provider import Provider
from src.Product import Product
from src.http_util import validate_http_status_code


_VERSION_LIST_URL = 'https://code.visualstudio.com/sha'
_EXTENSION_GALLERY_URL = 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery'
_DOWNLOAD_ENDPOINT = '/Microsoft.VisualStudio.Services.VSIXPackage'


class Vscode(Provider):
    @staticmethod
    def __get_vscode_latest(os_arch: str = 'win32-x64', channel: str = 'stable') -> str:
        response = requests.get(_VERSION_LIST_URL)
        versions = json.loads(response.text)['products']
        relevant_versions = [
            version for version in versions
            if version['platform']['os'] == os_arch and version['build'] == channel
        ]
        return relevant_versions[0]['name']

    @staticmethod
    def __generate_extension_gallery_headers(vscode_version) -> dict:
        return {
            'X-Market-Client-Id': vscode_version,
            'content-type': 'application/json',
            'Accept': 'application/json;api-version=3.0-preview.1',
        }

    @staticmethod
    def __generate_extension_gallery_body(extension_name: str, extension_version: str) -> dict:
        return {
            'filters': [{'criteria': [{'filterType': 7, 'value': extension_name}]}],
            'assetTypes': ['Microsoft.VisualStudio.Services.VSIXPackage'],
            'flags': 0x200 + 0x2,  # 0x200 - only latest; 0x2 - include files
        }

    @property
    def name(self):
        return 'vscode'

    @property
    @staticmethod
    def products(self):
        return 'vscode extensions'

    @property
    def file_ext(self):
        return 'vsix'

    def _resolve_product(self, product_name, product_version):
        if (product_version and product_version != 'latest'):
            raise NotImplementedError(
                'Vscode provider currently only supports providing latest version')
        try:
            vscode_version = Vscode.__get_vscode_latest()
            response = requests.post(
                _EXTENSION_GALLERY_URL,
                data=json.dumps(Vscode.__generate_extension_gallery_body(
                    product_name, product_version)),
                headers=Vscode.__generate_extension_gallery_headers(
                    vscode_version),
            )
            validate_http_status_code(
                response.status_code, self, product_name, product_version)
            response_payload = response.json()

            extension_latest_md = response_payload['results'][0]['extensions'][0]['versions'][0]
            version = extension_latest_md['version']
            download_url = extension_latest_md['fallbackAssetUri'] + \
                _DOWNLOAD_ENDPOINT
            self._logger.info('Resolved vscode extension {0} for vscode version {1} to version {2}'.format(
                product_name, vscode_version, version))
            return Product(self, product_name, version, download_url)
        except Exception as e:
            raise ValueError(product_name, Vscode.__get_vscode_latest()) from e
