from src.providers import Provider


def validate_http_status_code(status_code: int, provider: Provider, product_name: str, product_version: str) -> None:
    message = None
    if status_code == 404:
        message = 'Product not found {0}:{1}'
    if status_code > 399:
        message = 'Unknown HTTP error occurred {0}:{1}'

    if message:
        raise Exception(message.format(product_name, product_version))
