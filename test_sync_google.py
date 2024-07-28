import gspread
import config.const as const
from google.oauth2.service_account import Credentials

# 设置 Google Sheets API 配置
SCOPES = const.SCOPES
SERVICE_ACCOUNT_FILE = const.SERVICE_ACCOUNT_FILE  # replace your JSON file dir

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

gc = gspread.authorize(credentials)
sh = gc.open('Dashboard')  
worksheet = sh.get_worksheet(4)  # select the 4th sheet in you spreadsheet

# append row['Hello', 'World'] to your sheet
worksheet.append_row(['Hello', 'World'])
print("Data added successfully!")
