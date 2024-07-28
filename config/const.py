import configparser


config = configparser.ConfigParser()
config.read('config/config.ini')

# parser notion table configs
NOTION_API_TOKEN = config['notion']['NOTION_API_TOKEN']
NOTION_API_URL = 'https://api.notion.com/v1'
ACCOUNTING_DB_ID = config['notion']['ACCOUNTING_DB_ID']
BUDGET_DB_ID = config['notion']['BUDGET_DB_ID']

NOTION_HEADERS = {
    'Authorization': f'Bearer {NOTION_API_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}


# parser google sheet configs
SCOPES = config['google_sheet']['SCOPES'].split(',')
SERVICE_ACCOUNT_FILE = config['google_sheet']['SERVICE_ACCOUNT_FILE']