import argparse
import multiprocessing
import ssl
import os
from str2bool import str2bool


from src.providers.vscode import Vscode
from src.providers.npm import Npm
from src.products_reader import get_lines
from src.downloader import download
from src.packager import package

providers_as_args = {
    'vscode': {
        'help': 'specify if should download vscode extentions',
        'class': Vscode,
        'file_path': './vscode.list'
    },
    'npm': {
        'help': 'specify if should download npm packages',
        'class': Npm,
        'file_path': './npm.list'
    }
}
parser = argparse.ArgumentParser(description='CLI tool')
for provider_flag, provider_args in providers_as_args.items():
    parser.add_argument('--{0}'.format(provider_flag),
                    type=str2bool,
                    default=False,
                    help=provider_args['help'])
parser.add_argument('--concurrency', type=int, default=2,
                    help='Number of workers = concurrency * CPU_CORES_COUNT')
parser.add_argument('--proxy', type=str2bool, default=False,
                    help='Turn on if you use a proxy')
args = parser.parse_args()


def main() -> None:
    base_directory = './packages'
    resolved_products = []
    num_workers = args.concurrency * os.cpu_count()
    if args.proxy:
        ssl._create_default_https_context = ssl._create_unverified_context
    for arg, value in vars(args).items():
        if arg in providers_as_args and value:
            provider_args = providers_as_args[arg]
            products = get_lines(provider_args['file_path'])
            provider = provider_args['class']()
            provided_products, file_ext, registry = provider.provide(products)
            resolved_products += [(base_directory,
                                    registry,
                                    product_name,
                                    product_ver,
                                    file_ext,
                                    product_dl_url)
                                    for product_name, product_ver, product_dl_url in provided_products]
    with multiprocessing.Pool(num_workers) as pool:
        output_paths = pool.starmap(download, resolved_products)
        no_none = [path for path in output_paths if path]
        package(no_none)


if __name__ == "__main__":
    main()
