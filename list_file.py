def get_lines(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()
