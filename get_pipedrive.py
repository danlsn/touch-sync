import configparser

import pandas as pd
from pipedrive.client import Client

# Get Secret Info from Config File
config = configparser.ConfigParser()
config.read('config.ini')

# Load Pipedrive Client
client = Client(domain=config['PIPEDRIVE']['DOMAIN'])
client.set_api_token(config['PIPEDRIVE']['API_TOKEN'])


def get_all_deals(limit=200):
    deals = []
    # related_objects = []
    all_deals = client.deals.get_all_deals(params={'limit': f'{limit}'})
    deals.extend(all_deals['data'])
    # related_objects.extend(all_deals['related_objects'])
    pagination = all_deals['additional_data']['pagination']
    more_items_in_collection = pagination['more_items_in_collection']
    while more_items_in_collection:
        more_deals = client.deals.get_all_deals(params={
            'start': f"{pagination['next_start']}",
            'limit': f"{pagination['limit']}"}
        )
        deals.extend(more_deals['data'])
        # related_objects.extend(more_deals['related_objects'])
        pagination = more_deals['additional_data']['pagination']
        print(more_deals)
    print(all_deals)

    return all_deals


def get_custom_field_names():
    all_custom_fields = []
    custom_fields = client.deals.get_deal_fields()
    all_custom_fields.extend(custom_fields['data'])
    # related_objects.extend(all_deals['related_objects'])
    pagination = custom_fields['additional_data']['pagination']
    more_items_in_collection = pagination['more_items_in_collection']

    while more_items_in_collection:
        more_custom_fields = client.deals.get_deal_fields(params={
            'start': f"{pagination['next_start']}",
            'limit': f"{pagination['limit']}"}
        )
        all_custom_fields.extend(more_custom_fields['data'])
        # related_objects.extend(more_deals['related_objects'])
        more_items_in_collection = more_custom_fields['additional_data']['pagination']['more_items_in_collection']
        print(more_custom_fields)

    custom_field_names = {}
    for item in all_custom_fields:
        custom_field_names[f"{item['key']}"] = item
        item_dict = {
            f"{item['key']}": item
        }
    print(custom_field_names)

    return custom_field_names


def update_deal_field_names(deals: list):
    cfn_dict = get_custom_field_names()

    for deal in deals:
        deal['22c36030bb7745bf4fd80de923ecdf7f126b3de3'] = cfn_dict['22c36030bb7745bf4fd80de923ecdf7f126b3de3']['title']
        print()


user_fields = []
custom_fields = client.deals.get_deal_fields()['data']

for field in custom_fields:
    if field['edit_flag']:
        user_fields.append(field)

all_deals = []
for deal in get_all_deals(200)['data']:
    for field in user_fields:
        print(f"field={field}")
        print(deal[f"{field['key']}"])
        deal[f"{field['name']}"] = deal[f"{field['key']}"]
        # del deal[f"{field['key']}"]
    all_deals.append(deal)

df = pd.json_normalize(all_deals)
df.to_csv('output/pipedrive-deals.csv')
exit(0)

# deals.extend(all_deals['data'])
# pagination = all_deals['additional_data']['pagination']
# more_items_in_collection = pagination['more_items_in_collection']
# while more_items_in_collection is True:
#     next_start = pagination['next_start']
#     all_deals = client.deals.get_all_deals(params={'start': next_start})
#     deals.extend(all_deals['data'])
#     more_items_in_collection = pagination['more_items_in_collection']

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
# while activities['additional_data']['pagination']['more_items_in_collection'] is True: all_deals =
# client.activities.get_all_activities(params={'start': activities['additional_data']['pagination']['start']})
# activities['additional_data'] = all_deals.additional_data for item in all_deals['data']: activities['data'].append(
# item) if all_deals['additional_data']['pagination']['']

exit(0)
