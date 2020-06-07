import ssl
import sys
import os
import logging

from src import packagers, DAL
from src.command_line import args
from src.providers import get_providers


args_dict = vars(args)
providers = { provider.name: provider for provider in get_providers() }
databases = { db.name: db for db in DAL.get_databases() }

def get_logger(level=logging.DEBUG):
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s\t|\t%(levelname)s\t|\t%(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False    
    return logger

def main() -> None:
    logger = get_logger()
    num_workers = args.concurrency * os.cpu_count()
    if not args.strict_ssl:
        ssl._create_default_https_context = ssl._create_unverified_context

    logger.info('Connecting to Database')
    with databases[args.database](logger, args.database_args) as db:
        logger.info(f'Successfully connect to database of type {args.database}')

        logger.info('Started resolving providers')
        db_providers = [ provider.name for provider in db.get_providers() ]
        selected_providers = [ key for key in providers if args_dict[key] ]
        for provider in selected_providers:
            if provider not in db_providers:
                logger.warning(f'Provider {provider} not in database. It will be added')
                db.add_provider(providers[provider])
        logger.info('Successfully resolved providers')
        
        logger.info('Started resolving products')
        resolved_products = []
        for provider_name in selected_providers:
                logger.info(f'Started resolving products from provider {provider_name}')
                provider = providers[provider_name]
                requested_products = [ (product.name, product.version) for product in db.get_products(provider) ]
                logger.info(f'Found {len(requested_products)} products in DB for provider {provider_name}')
                provider_products = provider(logger).provide(requested_products)
                resolved_products += provider_products
                logger.info(f'Resolved {len(provider_products)} products for provider {provider_name}')
        logger.info('Successfully resolved products')

        resolved_products = [ product for product in resolved_products if not db.is_downloaded_before(product) ]
        logger.info(f'Found {len(resolved_products)} new products to download')

        if len(resolved_products) < 1:
            logger.info('No new products found. exiting')
            return

        logger.info('Started packaging resolved products')
        packager = packagers.get_packager(args.packager, **args_dict, logger=logger, num_workers=num_workers)
        packager.package(resolved_products)
        logger.info('Successfully packaged products')

        logger.info('Reporting to DB')
        for product in resolved_products:
            db.add_resolved_product(product)

        logger.info('Done')


if __name__ == "__main__":
    main()
