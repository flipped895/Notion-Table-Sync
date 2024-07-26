import configparser
import requests
import logging

# create configparser object
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# replace with your Notion API secret_key in config.ini
NOTION_API_TOKEN = config['DEFAULT']['NOTION_API_TOKEN']

# replace with your database ID in config.ini
ACCOUNTING_DB_ID = config['DEFAULT']['ACCOUNTING_DB_ID']
BUDGET_DB_ID = config['DEFAULT']['BUDGET_DB_ID']

# Notion API 基础URL
NOTION_API_URL = 'https://api.notion.com/v1'

headers = {
    'Authorization': f'Bearer {NOTION_API_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}


def get_database_items(database_id):
    url = f'{NOTION_API_URL}/databases/{database_id}/query'
    all_items = []
    start_cursor = None

    while True:
        payload = {}
        if start_cursor:
            payload['start_cursor'] = start_cursor
        response = requests.post(url, headers=headers, json=payload)

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


#  property_name = 'Total_by_Category'
def update_page_property(page_id, property_name, property_value):
    url = f'{NOTION_API_URL}/pages/{page_id}'
    data = {
        "properties": {
            property_name: {
                "number": property_value
            }
        }
    }
    logging.info(f'Updating page {page_id} property {property_name} with value {property_value}')
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code != 200:
        logging.error(f"Error updating page property: {response.json()}")
    return response.json()


def main():
    logging.info(f'Get accounting table items....')
    accounting_items = get_database_items(ACCOUNTING_DB_ID)
    logging.info(f'Get budget table items....')
    budget_items = get_database_items(BUDGET_DB_ID)
    total_by_category = dict()
    for account_item in accounting_items:
        account_category = account_item['properties']['Category']['select']['name']
        transaction = account_item['properties']['transaction']['formula']['number']
        if account_category not in total_by_category.keys():
            total_by_category[account_category] = 0
        total_by_category[account_category] += transaction

    budget_categories = list()
    for budget_item in budget_items:
        budget_categories.append(budget_item['properties']['Category']['select']['name'])
        budget_id = budget_item['id']
        logging.info(
            f'Updating category {budget_categories[-1]} in budget database with amount {total_by_category[budget_categories[-1]]}')
        update_page_property(budget_id, 'Total_by_Category', total_by_category[budget_categories[-1]])
    if set(budget_categories) != set(total_by_category.keys()):
        logging.info(
            f'budget_categories not in accounting database categories is {set(budget_categories) - set(total_by_category.keys())}')
        logging.info(
            f'accounting database categories not in budget_categories are {set(budget_categories) - set(total_by_category.keys())}')


if __name__ == '__main__':
    main()
