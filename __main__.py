from multiprocessing.pool import ThreadPool
import ssl
import sys
import os
import logging

from src.products_reader import get_lines
from src.Downloader import Downloader
from src.packager import package
from src.command_line import args
from src.providers import providers

providers = {provider['name']: provider['class'] for provider in providers}


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
    downloader = Downloader(args.temp_dir, logger=logger)
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
            product_names = get_lines(
                '{0}/{1}.list'.format(args.input_dir, provider.name))
            resolved_products += provider.provide(
                [(product_name, 'latest') for product_name in product_names])

    with ThreadPool(num_workers) as pool:
        logger.info('Started Downloading')
        downloaded_paths = pool.map(downloader.download, resolved_products)
        paths_to_bundle = [path for path in downloaded_paths if path]
        if len(paths_to_bundle) > 0:
            logger.info('Started packaging')
            package_name = package(paths_to_bundle, args.output_dir)
            logger.debug(
                'Finished packaging into file {0}'.format(package_name))
        else:
            logger.info('No new products - skipping packaging')


if __name__ == "__main__":
    main()
