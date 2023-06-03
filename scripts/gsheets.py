import os
from dotenv import load_dotenv
import gspread

load_dotenv('.env')

def load_sheet(file_name: str) -> gspread.Worksheet:
    try:
        gc = gspread.service_account(filename='./service_secrets.json')
        
        spreadsheet = gc.open(file_name)
        return spreadsheet.sheet1
    except Exception:
        print('scripts --> gsheets --> load_sheet failed')
        raise

def create_sheet(file_name: str) -> gspread.Worksheet:
    try:
        gc = gspread.service_account(filename='./service_secrets.json')

        spreadsheet = gc.create(file_name, os.environ['DATA_FOLDER_ID'])
        spreadsheet.share(os.environ['EMAIL'], perm_type='user', role='writer')
        return spreadsheet.sheet1
    except Exception:
        print('scripts --> gsheets --> create_sheet failed')
        raise