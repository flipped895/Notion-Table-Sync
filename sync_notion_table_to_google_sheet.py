from config import const
from notion.notion_database import get_database_items
import gspread
from google.oauth2.service_account import Credentials


def main():
    credentials = Credentials.from_service_account_file(
        const.SERVICE_ACCOUNT_FILE, scopes=const.SCOPES)

    gc = gspread.authorize(credentials)
    sh = gc.open('Dashboard')
    worksheet = sh.get_worksheet(4)  # 选择表格中的第一个工作表

    current_budget_table = get_database_items(const.BUDGET_DB_ID)
    update_data = list()
    for item in current_budget_table:
        update_data.append([item['properties']['Category']['select']['name'],
                            item['properties']['budget']['number'],
                            item['properties']['Total_by_Category']['number']])
    worksheet.update(f'A2:C10', update_data)


if __name__ == '__main__':
    main()
