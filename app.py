
import json
import asyncio
from aiohttp import ClientSession, web


async def get_weather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            try:
                return weather_json["weather"][0]["main"]
            except KeyError:
                return "No Data"

async def get_translation(text, source, target):
    async with ClientSession()as session:
        url = 'https://libretranslate.de/translate'
        data = {'q': text, 'source': source, 'target': target, 'format': 'text'}

        async with session.post(url, json=data) as response:
            translate_json = await response.json()

            try:
                return translate_json['translatedText']
            except KeyError:
                print(1)
                return text

async def handle(request) -> "web.Response":
    city_uk = request.rel_url.query['city']
    city_en = await get_translation(city_uk, 'uk', 'en')


    weather_en = await get_weather(city_en)
    weather_uk = await get_translation(weather_en, 'en', 'uk')

    result = {'city': city_uk, 'weather': weather_uk}

    return web.Response(text=json.dumps(result, ensure_ascii=False))

async def main():
    app = web.Application()
    app.add_routes([web.get('/weather', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", "8080")
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())