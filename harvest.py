import configparser
import json
import requests

config = configparser.ConfigParser()
config.read('config.ini')

headers = {
    'User-Agent': 'Python Harvest API (danlsn/touch-sync)',
    'Authorization': f'''Bearer {config['HARVEST']['ACCESS_TOKEN']}''',
    'Harvest-Account-ID': f'''{config['HARVEST']['ACCOUNT_ID']}'''
}


def get_all_projects():
    projects = list()
    url = 'https://api.harvestapp.com/v2/projects'
    r = requests.get(url, headers=headers)
    j = json.loads(r.text)
    projects.extend(j['projects'])
    while j['links']['next'] is None:
        return projects


get_all_projects()
