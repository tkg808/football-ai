import os
from typing import List
from .gsheets import load_sheet, create_sheet
import aiohttp

async def get_new_names(year: int) -> None:
    url = f'https://api.collegefootballdata.com/teams/fbs?year={year}'
    headers = {
        'Authorization': f'Bearer {os.environ["CFBD_KEY"]}'
    }
    file_name = f'{year}_names'
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                names = [[val['school']] for val in data]

                worksheet = create_sheet(file_name)
                worksheet.update(names)
        except Exception:
            print('cfbd_names --> get_team_names --> Fetch failed')
            raise

async def get_saved_names(year: int) -> List[str]:
    try:
        return load_sheet(f'{year}_names').col_values(1)
    except Exception:
        print('scripts --> cfbd_names --> get_saved_names failed')