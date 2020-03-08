import argparse
import multiprocessing
import ssl
from typing import List, Callable
from str2bool import str2bool


from src.providers.Vscode import Vscode
from src.providers.Npm import Npm
from src.products_reader import get_lines
from src.downloader import download
from src.packager import package


parser = argparse.ArgumentParser(description='CLI tool')
parser.add_argument('--vscode', type=str2bool, default=False,
                    help='specify if should download vscode extentions')
parser.add_argument('--npm', type=str2bool, default=True,
                    help='specify if should download npm packages')
args = parser.parse_args()


def main() -> None:
    base_directory = './packages'
    resolved_products = []
    if args.npm:
        npm = Npm()
        products = get_lines('./npm.list')
        npm_packages_dl_urls, file_ext, registry = npm.provide(products)
        resolved_products = [(base_directory, registry, pkg_name, pkg_ver, file_ext, pkg_dl_url) for pkg_name, pkg_ver, pkg_dl_url in npm_packages_dl_urls]
    elif args.vscode:
        vscode = Vscode()
        products = get_lines('./vscode.list')
        vscode_extentions_dl_info, file_ext, registry = vscode.provide(products)
        resolved_products += [(base_directory, registry, ext_name, ext_ver, file_ext, ext_dl_url) for ext_name, ext_ver, ext_dl_url in vscode_extentions_dl_info ]

    with multiprocessing.Pool(8) as pool:
        output_paths = pool.starmap(download, resolved_products)
        no_none = list(filter(lambda x: x is not None, output_paths))
        package(no_none)


if __name__ == "__main__":
    main()
