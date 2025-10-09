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

