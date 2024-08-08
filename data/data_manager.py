from datetime import datetime
import threading
from data.google_sheets_manager import GoogleSheetsManager
from utils.config import DATA_CACHE_EXPIRY

class DataManager:
    def __init__(self):
        self.df = None
        self.last_fetch_time = None
        self.lock = threading.Lock()
        self.google_sheets_manager = GoogleSheetsManager()

    def get_data(self):
        with self.lock:
            if self.df is None or (datetime.now() - self.last_fetch_time).total_seconds() > DATA_CACHE_EXPIRY:
                self.df = self.google_sheets_manager.get_sheet_data()
                self.last_fetch_time = datetime.now()
            return self.df
