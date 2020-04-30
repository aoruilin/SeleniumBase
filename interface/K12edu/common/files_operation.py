import os


def file_write(path, file_name, content):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f'{path}{file_name}', 'wb') as f:
        f.write(content)
