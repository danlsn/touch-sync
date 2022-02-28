import airtable
import configparser
import pandas as pd


# Get Secret Info from Config File
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['AIRTABLE']['API_KEY']
base_id = config['AIRTABLE']['BASE_ID']

# Create Instance of Airtable()
table = airtable.Airtable(base_id, 'Index', api_key)

# print(f"{table!r}")

all_records = table.get_all()

exit(0)
