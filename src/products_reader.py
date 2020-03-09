from typing import List


def get_lines(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return [line for line in file.read().splitlines() if len(line) > 0]
