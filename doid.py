import requests
import time

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


search_cache = {}
get_cache = {}

def search(name: str):
    if name in search_cache:
        return search_cache[name]

    search_url = 'https://disease-ontology.org/search'

    params = {
        'q': name,
        'adv_search': False,
        'field-1': 'name',
        'subset-1': 'DO_AGR_slim',
        'relation-1': 'adjacent to',
        'tree': 'obo'
    }
    
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        text = response.text
        
        soup = BeautifulSoup(text, 'html.parser')
        doid_elements = soup.find_all(class_='tbl-doid')
        doids = [element.get_text() for element in doid_elements]
        search_cache[name] = doids
        return doids
    return []


def get_root(data: list):
    children = data[0]
    if children.get('children'):
        return get_root(children.get('children'))
    else:
        return children['id']


def fetch_data(doid):
    if doid in get_cache:
        return get_cache[doid]

    url = 'https://disease-ontology.org/query_tree'
    params = {
        '_dc': int(time.time()),
        'search': True,
        'tree': 'obo',
        'node': doid
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        get_cache[doid] = get_root(data).split('-')
        return get_root(data).split('-')


def get_path_to_root(ids: list):
    paths_to_root = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_data, ids)
        for result in results:
            if result:
                paths_to_root.append(result)
    return paths_to_root