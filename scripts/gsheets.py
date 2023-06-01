import gspread

def load_sheet(file_name: str):
    gc = gspread.service_account(filename='./service_secrets.json')

    worksheet = gc.open(file_name).sheet1
    return worksheet.get_all_records() 