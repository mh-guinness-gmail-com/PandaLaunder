import argparse
import tempfile
import re
from str2bool import str2bool

from src import __version__ as version
from src.packagers import packager_type_codes, default_packager_type_code
from src.providers import get_providers_classes


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
__parser.add_argument('--version', action='version',
                    version='{}'.format(version),
                    help='show the version number and exit')

packager_type_helps = [
    '{0} - use{1}'.format(code, re.sub('([A-Z])', ' \\g<0>', packager_type.__name__))
    for code, packager_type in packager_type_codes.items()
]
__parser.add_argument('--packager', '-p', type=str, default=default_packager_type_code, choices=packager_type_codes.keys(),
                      help='Which packager to use. options are:\n{0}'.format('\n'.join(packager_type_helps)))

for provider in get_providers_classes():
    __parser.add_argument('--{0}'.format(provider.name),
                          action='store_true',
                          default=False,
                          help='specify if should download {0}'.format(provider.products))

args = __parser.parse_args()
