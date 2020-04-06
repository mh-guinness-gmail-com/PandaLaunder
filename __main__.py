import multiprocessing
import ssl
import os

from src.products_reader import get_lines
from src.Downloader import Downloader
from src.packager import package
from src.command_line import args
from src.providers import providers
from src.loggers import ConsoleLogger

providers = {provider['name']: provider['class'] for provider in providers}


def main() -> None:
    logger = ConsoleLogger()
    downloader = Downloader(args.temp_dir, logger=logger)
    num_workers = args.concurrency * os.cpu_count()
    if not args.strict_ssl:
        ssl._create_default_https_context = ssl._create_unverified_context

    resolved_products = []
    for provider_name, value in vars(args).items():
        if provider_name in providers and value == True:
            provider = providers[provider_name](logger)
            product_names = get_lines(provider.name)
            resolved_products += provider.provide(
                [(product_name, 'latest') for product_name in product_names])

    with multiprocessing.Pool(num_workers) as pool:
        output_paths = [path for path in pool.starmap(
            downloader.download, resolved_products) if path]
        package(output_paths, args.output_dir)


if __name__ == "__main__":
    main()
