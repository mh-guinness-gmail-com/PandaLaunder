import multiprocessing
import ssl
from typing import List, Callable


import packager
import lib.providers.vscode
from src.products_reader import get_lines


def main() -> None:
    base_directory = './packages'
    '''
    1. פרזור הרשימה
    2. Resolve dependency
    3. הבאת גירסאות (או כחלק משלב 2?)
    4. בדיקת שינויים
    5. הבאת לינקים
    6. הורדה
    7. כיווץ
    '''
    packager.package(downloaded)


if __name__ == "__main__":
    main()
