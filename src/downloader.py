import os
import urllib.request


def __get_output_file_path(base_dir: str, registry_name: str, package_name: str, version_name: str, package_ext: str) -> str:
    package_dir = os.path.join(base_dir, registry_name, package_name)
    try:
        os.makedirs(package_dir)
    except:
        pass
    return os.path.join(package_dir, version_name + '.' + package_ext)


def download(base_dir: str, registry_name: str, package_name: str, version_name: str, package_ext: str, url: str, overwrite: bool = False) -> str:
    output_path = __get_output_file_path(base_dir, registry_name, package_name, version_name, package_ext)
    if overwrite or not os.path.isfile(output_path):
        urllib.request.urlretrieve(url, output_path)
        return output_path
