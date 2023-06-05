import os
from typing import List
import pandas as pd
import asyncio
from asyncio import Queue
import aiohttp
from .gsheets import load_sheet, create_sheet
from .cfbd_names import get_saved_names

async def get_new_drives(year: int) -> None:
    try:
        results = []
        schools = await get_saved_names(year)
        que = Queue()
        for school in schools:
            await que.put(school)

        async with aiohttp.ClientSession() as session:
            tasks = []
            MAX_REQS = 5           
            for _ in range(MAX_REQS):
                task = asyncio.create_task(process_que(que, session, year, results))
                tasks.append(task)

            # Waits until all tasks in the que have been processed
            await que.join()

            # Adds sentinel null values to break out of proccessing loop
            for _ in range(MAX_REQS):
                await que.put(None)

            # Processes tasks
            await asyncio.gather(*tasks)
        
        # Flatten results
        drives = []
        for rows in results:
            drives.extend(rows)

        df = pd.DataFrame(drives)
        df = flatten_time_columns(df)

        # Save to Google Drive
        file_name = f'{year}_drives'
        worksheet = create_sheet(file_name)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        print('scripts --> cfbd_drives --> get_new_drives failed')
        raise e


async def process_que(que: Queue, session: aiohttp.ClientSession, year: int, results: List) -> None:
    while not que.empty():
        school = await que.get()
        if not school:
            break
        try:
            result = await get_team_drives(school, year, session)
            results.append(result)
        except Exception as e:
            print('scripts --> cfbd_drives --> process_que failed')
            raise e
        finally:
            que.task_done()


async def get_team_drives(team: str, year: int, session: aiohttp.ClientSession) -> List[any]:
    url = f'https://api.collegefootballdata.com/drives?seasonType=regular&year={year}&team={team}&offense={team}'
    headers = {
        'Authorization': f'Bearer {os.environ["CFBD_KEY"]}'
    }

    try:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            print(f'team: {team} -> Status: {response.status}')
            return data
    except Exception as e:
        print('scripts --> cfbd_drives --> get_team_drives failed')
        raise e


async def get_saved_drives(year: int) -> List[dict]:
    try:
        return load_sheet(f'{year}_drives').get_all_records()
    except Exception as e:
        print('scripts --> cfbd_drives --> get_saved_drives failed')
        raise e


def flatten_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    try:
        for col in df.columns:
            if df[col].dtype == 'O' and isinstance(df[col].iloc[0], dict):
                df[col] = df[col].apply(lambda x: x['minutes']*60 + x['seconds'])
        return df
    except Exception as e:
        print('scripts --> cfbd_drives --> flatten_time_columns failed')
        raise e
