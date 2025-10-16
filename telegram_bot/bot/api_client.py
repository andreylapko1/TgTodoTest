import json

import aiohttp
import telegram_bot.bot.config as cfg

class DjangoAPIClient:
    def __init__(self):
        self.base_url = cfg.API_URL


    async def get_categories(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.base_url + 'categories/', )
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []

    async def create_task(self,username: str,  title: str, description: str, category: str, due_date: str, telegram_id: str | int):

        payload = {
            'telegram_id': telegram_id,
            'username': username,
            "title": title,
            "description": description,
            "category": category,
            "due_date": due_date
        }
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                self.base_url + 'tasks/create/',
                json=payload
            )
            if response.status == 201:
                print('ASDASD')
                return True
            else:
                response = await response.json()
                with open('resp', 'w') as file:
                    file.write(json.dumps(response))
                return False

