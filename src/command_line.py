import argparse
import tempfile
from str2bool import str2bool


from src.providers import providers


__parser = argparse.ArgumentParser()

__parser.add_argument('--concurrency-per-core', '-c', type=int, default=2, dest='concurrency',
                      help='Number of workers = concurrency * CPU_CORES_COUNT')
__parser.add_argument('--input-dir', '-i', type=str, default='./in',
                      help='Base directory where list files are located')
__parser.add_argument('--output-dir', '-o', type=str, default='./out',
                      help='Base directory to place bundled zip file in')
__parser.add_argument('--packager', '-p', type=str, default='m',
                      help='Which packager to use (m for memory based packager or f for FS based packager)')
__parser.add_argument('--temp-dir', '-t', type=str, default=tempfile.TemporaryDirectory().name,
                      help='Base directory to place all downloaded files before bundling. Applies only for FS based packager')
__parser.add_argument('--strict-ssl', type=str2bool, default=True,
                      help='False disables ssl certificate checks')

for provider in providers:
    __parser.add_argument('--{0}'.format(provider['name']),
                          action='store_true',
                          default=False,
                          help='specify if should download {0}'.format(provider['products']))

args = __parser.parse_args()
