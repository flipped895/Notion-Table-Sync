import configparser
import logging
from config import const
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# create configparser object
config = configparser.ConfigParser()
config.read('config/config.ini')


def get_database_items(database_id):
    url = f'{const.NOTION_API_URL}/databases/{database_id}/query'
    all_items = []
    start_cursor = None

    while True:
        payload = {}
        if start_cursor:
            payload['start_cursor'] = start_cursor
        response = requests.post(url, headers=const.NOTION_HEADERS, json=payload)

        response_data = response.json()
        if response.status_code != 200:
            logging.error(f"Error fetching database items: {response.json()}")
        # get current page data
        results = response_data.get('results', [])
        all_items.extend(results)

        # check if there is more data
        if not response_data.get('has_more', False):
            break
        start_cursor = response_data.get('next_cursor', None)

    return all_items


def update_page_property(page_id, property_name, property_value):
    url = f'{const.NOTION_API_URL}/pages/{page_id}'
    data = {
        "properties": {
            property_name: {
                "number": property_value
            }
        }
    }
    logging.info(f'Updating page {page_id} property {property_name} with value {property_value}')
    response = requests.patch(url, headers=const.NOTION_HEADERS, json=data)
    if response.status_code != 200:
        logging.error(f"Error updating page property: {response.json()}")
    return response.json()
