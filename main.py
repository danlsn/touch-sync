import configparser
from pipedrive.client import Client


# Get Secret Info from Config File
config = configparser.ConfigParser()
config.read('config.ini')

print(config.sections())
client = Client(domain=config['PIPEDRIVE']['DOMAIN'])
client.set_api_token(config['PIPEDRIVE']['API_TOKEN'])

deals = list()

response = client.deals.get_all_deals()
deals.extend(response['data'])
pagination = response['additional_data']['pagination']
more_items_in_collection = pagination['more_items_in_collection']
while more_items_in_collection is True:
    next_start = pagination['next_start']
    response = client.deals.get_all_deals(params={'start': next_start})
    deals.extend(response['data'])
    more_items_in_collection = pagination['more_items_in_collection']

# activities = dict()
# activities['data'] = list()
# activities['additional_data'] = dict()
# activities['additional_data']['pagination'] = {
#     "start": 0,
#     "limit": 100,
#     "more_items_in_collection": True,
#     'next_start': 0
# }
#
# while activities['additional_data']['pagination']['more_items_in_collection'] is True:
#     response = client.activities.get_all_activities(params={'start': activities['additional_data']['pagination']['start']})
#     activities['additional_data'] = response.additional_data
# for item in response['data']:
#     activities['data'].append(item)
# if response['additional_data']['pagination']['']

exit(0)

