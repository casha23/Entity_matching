import html
import os
import re

from doid import get_path_to_root, search


def string_replace(string: str):
    string = html.unescape(string)
    string = string.replace("/", " ")
    string = string.replace("´", "'")
    string = string.replace("`", "'")
    
    patt = re.compile(r'(\w+)([+-])\s\b')
    string = re.sub(patt, r'\2\1 ', string)
    string = re.sub(r'\s+', ' ', string)
    return string


def write_result(string: str, paths: list):
    file_path = os.path.join(os.path.dirname(__file__), 'results.txt')

    with open(file_path, 'a') as file:
        file.write(f"{string} {paths}\n")

  
def proccess_row(row):
    string = ' '.join(row)
    string = string_replace(string)
    ids = search(string)
    paths = get_path_to_root(ids)
    write_result(string, paths)
