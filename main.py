import argparse
import multiprocessing
import ssl
from typing import List, Callable


from src.providers.Vscode import Vscode
from src.providers.Npm import Npm
from src.products_reader import get_lines
from src.downloader import download


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='CLI tool')
parser.add_argument('--vscode', type=str2bool, default=False,
                    help='specify if should download vscode extentions')
parser.add_argument('--npm', type=str2bool, default=True,
                    help='specify if should download npm packages')
args = parser.parse_args()


def main() -> None:
    base_directory = './packages'
    will_be_downloaded = []
    if args.npm:
        npm = Npm()
        products = get_lines('./npm.list')
        npm_packages_dl_urls, file_ext, registry = npm.provide(products)
        will_be_downloaded = [(base_directory, registry, pkg_name, pkg_ver, file_ext, pkg_dl_url) for pkg_name, pkg_ver, pkg_dl_url ]
    elif args.vscode:
        vscode = Vscode()
        products = get_lines('./vscode.list')
        vscode_extentions_dl_info, file_ext, registry = vscode.provide(products)
        will_be_downloaded += [(base_directory, registry, ext_name, ext_ver, file_ext, ext_dl_url) for ext_name, ext_ver, ext_dl_url in vscode_extentions_dl_info ]

    with multiprocessing.Pool(8) as pool:
        # deps_of_deps is a 2d array of results
        output_paths = pool.starmap(download, will_be_downloaded)


if __name__ == "__main__":
    main()
