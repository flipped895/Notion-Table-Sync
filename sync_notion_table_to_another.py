import configparser
import logging
import notion.notion_database as notion_database
from datetime import datetime
from config import const as notion_const


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # create configparser object
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    #  property_name = 'Total_by_Category'
    logging.info(f'Get accounting table items....')
    accounting_items = notion_database.get_database_items(notion_const.ACCOUNTING_DB_ID)
    logging.info(f'Get budget table items....')
    budget_items = notion_database.get_database_items(notion_const.BUDGET_DB_ID)
    total_by_category = dict()

    # get account_items, figure out total amount by category and store results to total_by_category dict
    for account_item in accounting_items:
        account_category = account_item['properties']['Category']['select'].get('name', 'Unknown')  # This will safely return 'Unknown' if any of the keys are missing or if the value is None.
        transaction = account_item['properties']['transaction']['formula']['number']
        if account_category not in total_by_category.keys():
            total_by_category[account_category] = 0

        # filter current month transaction
        current_month = datetime.now().month
        # print(account_item['properties']['Date']['date']['start'])
        # the fromisoformat method will correctly parse the entire date and time, including the time zone offset,
        # into a datetime object. This avoids the ValueError you encountered with strptime.
        date_object = datetime.fromisoformat(account_item['properties']['Date']['date']['start'])
        if date_object.month == current_month:
            total_by_category[account_category] += transaction

    # store total_by_category to budget database
    budget_categories = list()
    for budget_item in budget_items:
        budget_categories.append(budget_item['properties']['Category']['select']['name'])
        budget_id = budget_item['id']
        logging.info(
            f'Updating category {budget_categories[-1]} in budget database with amount {total_by_category[budget_categories[-1]]}')
        notion_database.update_page_property(budget_id, 'Total_by_Category', total_by_category[budget_categories[-1]])

    if set(budget_categories) != set(total_by_category.keys()):
        logging.info(
            f'budget_categories not in accounting database categories is {set(budget_categories) - set(total_by_category.keys())}')
        logging.info(
            f'accounting database categories not in budget_categories are {set(budget_categories) - set(total_by_category.keys())}')


if __name__ == '__main__':
    main()
