import multiprocessing
import ssl
from typing import List, Callable

import downloader
import packager
import vscode

def __get_lines(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return list(filter(lambda x: len(x) > 0, file.read().splitlines()))


def __download_single_package(base_directory: str, registry_name: str, package_name: str, package_ext: str, package_getter: Callable) -> str:
    (version_name, url) = package_getter(package_name)
    return downloader.download(base_directory, registry_name, package_name, version_name, package_ext, url)


def __download_packages(base_directory: str, registry_name: str, package_ext: str, package_getter: Callable, package_list_file: str) -> List[str]:
    package_names = [
        (base_directory, registry_name, package_name, package_ext, package_getter)
        for package_name in  __get_lines(package_list_file)
    ]
    with multiprocessing.Pool(16) as pool:
        downloaded = pool.starmap(__download_single_package, package_names)
    return downloaded

 
ssl._create_default_https_context = ssl._create_unverified_context

def main() -> None:
    base_directory = './packages'
    downloaded = __download_packages(base_directory, 'vscode', 'vsix', vscode.get_extension, 'vscode.list')
    # ToDo save to some (file based?) DB all downloaded files and clean downloads
    packager.package(downloaded)

if __name__ == "__main__":
    main()
