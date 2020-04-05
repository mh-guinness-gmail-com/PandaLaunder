from typing import List, Tuple
import requests
import multiprocessing
import itertools
import semver
import os

from src.providers.Provider import Provider

NPM_REGISTRY_URL = 'https://registry.npmjs.org/'


def _get_version_package_payload(package_name: str, version: str) -> dict:
    response = requests.get(NPM_REGISTRY_URL + package_name)
    if response.status_code == 404:
        raise Exception('Module not found {0}:{1}'.format(package_name, version))
    if response.status_code > 399:
        raise Exception('Unknown error occurred {0}:{1}'.format(package_name, version))
    response_payload = response.json()
    if version == 'latest':
        version = response_payload['dist-tags']['latest']
    satisfied_version = semver.max_satisfying(list(response_payload['versions'].keys()), version, loose=False)
    if version is None:
        raise Exception('Version was not found for {0}:{1}'.format(package_name, version))
    print('Matched {0}@{1} to specific version {2}'.format(package_name, version, satisfied_version))
    version = satisfied_version
    return version, response_payload['versions'][version]


def _get_deps(package_name: str, version: str, should_download_dev_deps=False) -> List[Tuple[str, str, dict]]:
    _, version_response_payload = _get_version_package_payload(package_name, version)
    deps = []
    if 'dependencies' in version_response_payload:
        deps += version_response_payload['dependencies'].items()
    if should_download_dev_deps and 'devDependencies' in version_response_payload:
        deps += version_response_payload['devDependencies'].items()
    return [(pkg_name, *(_get_version_package_payload(pkg_name, ver))) for pkg_name, ver in deps]


class Npm(Provider):
    def __init__(self):
        """
        Initialize an npm package Provider
        """
        Provider.__init__(self)
        self.file_ext = 'tgz'
        self.npm_registry_name = 'npmjs'

    def provide(self, products):
        packages = [(pkg_name, 'latest') for pkg_name in products]
        cache = []
        deps = []
        for pkg_name, pkg_ver_node_semver in packages:
            deps += _get_deps(pkg_name, pkg_ver_node_semver)

        def is_in_cache_fn(dep):
            name = dep[0]
            ver = dep[1]
            for (cache_pkg_name, cache_ver, _) in cache:
                if cache_pkg_name == name and cache_ver == ver:
                    print('cache hit {0}:{1}'.format(cache_pkg_name, cache_ver))
                    return True
            return False

        with multiprocessing.Pool(os.cpu_count()) as pool:
            while len(deps) > 0:
                sliced_deps = [(x, y) for x, y, z in deps]
                # deps_of_deps is a 2d array of results
                deps_of_deps = pool.starmap(_get_deps, sliced_deps)
                # flatten
                deps_of_deps = list(itertools.chain(*deps_of_deps))
                cache += deps
                deps = [dep for dep in deps_of_deps if not is_in_cache_fn(dep)]
        return [(cache_pkg_name, cache_ver, response['dist']['tarball']) for cache_pkg_name, cache_ver, response in cache], self.file_ext, self.npm_registry_name
