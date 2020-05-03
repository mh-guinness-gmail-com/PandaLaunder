import ssl
import sys
import os
import logging

from src import packagers
from src.products_reader import get_lines
from src.command_line import args
from src.providers import get_providers_classes
from src.providers.Vscode import Vscode
from src.DAL.db import get_packages_by_provider

providers = {provider['name']: provider['class'] for provider in get_providers_classes()}


def get_logger(level=logging.DEBUG):
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s\t|\t%(levelname)s\t|\t%(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger


def main() -> None:
    logger = get_logger()
    num_workers = args.concurrency * os.cpu_count()
    if not args.strict_ssl:
        ssl._create_default_https_context = ssl._create_unverified_context

    resolved_products = []
    logger.info('Started resolving products')
    for provider_name, value in vars(args).items():
        if provider_name in providers and value:
            logger.info(
                'Started resolving products from provider {0}'.format(provider_name))
            provider = providers[provider_name](logger)
            product_names = [package['name'] for package in get_packages_by_provider(provider.name)]
            resolved_products += provider.provide(
                [(product_name, 'latest') for product_name in product_names])
    
    packager = packagers.get_packager(args.packager, **vars(args), logger=logger, num_workers=num_workers)
    packager.package(resolved_products)


if __name__ == "__main__":
    main()
