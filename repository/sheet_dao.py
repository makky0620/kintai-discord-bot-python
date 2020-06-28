import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class SheetDao:
    def __init__(self):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.environ.get('KEY_FILE_NAME'), scope)
        gc = gspread.authorize(credentials)

        #共有設定したスプレッドシートのシート1を開く
        self.workbook = gc.open_by_key(os.environ.get('SPREADSHEET_KEY'))

    def find_sheet(self):
        return self.workbook.sheet1

    def register(self, record):
        sheet = self.workbook.sheet1
        sheet.insert_row(list(record.values()), index=2)

    def update_by_id(self, user_id, record):
        sheet = self.workbook.sheet1

        row_idx = [cell.row for cell in sheet.findall(str(user_id))]
        rows = [sheet.range(idx, 1, idx, 5) for idx in row_idx]
        target_cell_list = [row for row in rows if row[3].value == ''][0]
        target_cell_list[3].value = record['end']

        sheet.update_cells(target_cell_list)
