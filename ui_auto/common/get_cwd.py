import os
from pathlib import Path


def get_absolute_path(dir_name):
    now_path = Path('.').absolute()
    while now_path.name != dir_name:
        now_path = now_path.parent

    return now_path


def get_str_path():
    now_path = os.path.abspath(os.getcwd())

    return now_path
