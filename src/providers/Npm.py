from typing import List, Tuple
import requests
import semver


from .Provider import Provider
from src.Product import Product
from src.http_util import validate_http_status_code


NPM_REGISTRY_URL = 'https://registry.npmjs.org'


class Npm(Provider):
    @property
    @staticmethod
    def name():
        return 'npm'

    @property
    @staticmethod
    def products():
        return 'npm packages'

    @property
    @staticmethod
    def file_ext():
        return 'tgz'

    def _resolve_product(self, product_name, product_version):
        response = requests.get(
            '{0}/{1}'.format(NPM_REGISTRY_URL, product_name))
        validate_http_status_code(
            response.status_code, self, product_name, product_version)
        response_payload = response.json()

        version = product_version
        if product_version == 'latest':
            version = response_payload['dist-tags']['latest']
        if version is None:
            raise Exception('Version was not found for {0}:{1}'.format(
                product_name, product_version))

        all_versions = list(response_payload['versions'].keys())
        version = semver.max_satisfying(all_versions, version, loose=False)
        self._logger.info('Resolved npm package {0}@{1} to version {2}'.format(
            product_name, product_version, version))
        download_url = response_payload['versions'][version]['dist']['tarball']
        return Product(Npm, product_name, version, download_url)

    def _get_dependencies(self, product: Product, *, get_dependencies=True, get_dev_dependencies=False) -> List[Tuple[str, str]]:
        response = requests.get(
            '{0}/{1}/{2}'.format(NPM_REGISTRY_URL, product.name, product.version))
        validate_http_status_code(
            response.status_code, self, product.name, product.version)
        response_payload = response.json()

        dependencies = []
        if get_dependencies and 'dependencies' in response_payload:
            dependencies += response_payload['dependencies'].items()
        if get_dev_dependencies and 'devDependencies' in response_payload:
            dependencies += response_payload['devDependencies'].items()

        return list(dependencies)
