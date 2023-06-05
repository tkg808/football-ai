from dotenv import load_dotenv
from scripts.gsheets import load_sheet, create_sheet
from scripts.cfbd_drives import get_new_drives, get_saved_drives
from scripts.cfbd_names import get_new_names, get_saved_names
import time
import datetime
import asyncio

load_dotenv('.env')
print('Hello from main.py')

''' ===== Fetch all drives and save to GDrive ===== '''
try:
    start = time.time()
    asyncio.run(get_new_drives(2022))
finally:
    total = time.time() - start
    print(f'Total time: {datetime.timedelta(seconds=total)}')
    
''' ===== Load sheet from GDrive as DataFrame ===== '''
# df = pd.DataFrame(load_sheet('2022_drives.json').get_all_records())
# print(len(df))
# print(df.columns)
# print(df.dtypes)