import argparse
import tempfile
import re
from str2bool import str2bool

from src import __version__ as version
from src import DAL
from src.packagers import packager_type_codes, default_packager_type_code
from src.providers import get_providers


__parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

__parser.add_argument('--concurrency-per-core', '-c', type=int, default=2, dest='concurrency',
                      help='Number of workers = concurrency * CPU_CORES_COUNT')
__parser.add_argument('--input-dir', '-i', type=str, default='./in',
                      help='Base directory where list files are located')
__parser.add_argument('--output-dir', '-o', type=str, default='./out',
                      help='Base directory to place bundled zip file in')
__parser.add_argument('--temp-dir', '-t', type=str, default=tempfile.TemporaryDirectory().name,
                      help='Base directory to place all downloaded files before bundling. Applies only for FS based packager')
__parser.add_argument('--strict-ssl', type=str2bool, default=True,
                      help='False disables ssl certificate checks')
__parser.add_argument('--version', '-v', action='version',
                      version='{}'.format(version),
                      help='show the version number and exit')

# Database
__parser.add_argument('--database', type=str, default=DAL.default,
                      choices=[db.name for db in DAL.get_databases()],
                      help='Specify used database')
__parser.add_argument('--database-args', type=str,
                      help='Specify arguments for used database')

# Providers
for provider in get_providers():
    __parser.add_argument(f'--{provider.name}',
                          action='store_true',
                          default=False,
                          help=f'specify if should download {provider.products}')

# Packager
packager_type_helps = [
    f'{code} - use {re.sub('([A-Z])', ' \\g<0>')}'
    for code, packager_type in packager_type_codes.items()
]
__parser.add_argument('--packager', '-p', type=str, default=default_packager_type_code, choices=packager_type_codes.keys(),
                      help=f'Which packager to use. options are:\n{'\n'.join(packager_type_helps))}')

args = __parser.parse_args()
