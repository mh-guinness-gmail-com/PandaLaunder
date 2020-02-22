from typing import List

def get_lines(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return list(filter(lambda x: len(x) > 0, file.read().splitlines()))
