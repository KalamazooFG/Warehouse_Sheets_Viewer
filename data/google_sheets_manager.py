import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from utils.config import SPREADSHEET_ID, RANGE_NAME, CREDS_PATH

class GoogleSheetsManager:
    def __init__(self):
        self._cached_creds = None

    def get_credentials(self):
        if self._cached_creds is None:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/drive'
            ]
            if os.path.exists(CREDS_PATH):
                self._cached_creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scopes)
            else:
                raise Exception('Make sure you have your credentials.json file in your working directory.')
        return self._cached_creds

    def get_google_sheet(self):
        creds = self.get_credentials()
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.worksheet(RANGE_NAME)
        return worksheet

    def get_sheet_data(self):
        worksheet = self.get_google_sheet()
        values = worksheet.get_all_values()
        df = pd.DataFrame(values[1:], columns=values[0])
        df = df.iloc[:5, [3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]]
        df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
        return df
