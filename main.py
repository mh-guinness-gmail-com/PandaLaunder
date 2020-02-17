import multiprocessing
import ssl

import extension
import list_file

ssl._create_default_https_context = ssl._create_unverified_context
def main():
    extensions = list_file.get_lines('./extensions.list')

    with multiprocessing.Pool(16) as pool:
        pool.map(extension.get_extension, extensions)

if __name__ == "__main__":
    main()
