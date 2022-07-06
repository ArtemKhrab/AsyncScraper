
import os
import asyncio
from arsenic import get_session, keys, browsers, services
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from requests_html import HTML
import itertools
import re
import time
import pathlib


async def extract_id(url_path):
    regex = r"https:\/\/rozetka\.com\.ua\/(?P<name>[\w-]+)\/p(?P<id>\d+)"
    group = re.match(regex, url_path)
    if not group:
        return None, None
    return group["id"], group["name"]


async def scraper(url):
    
    service = services.Chromedriver(binary="./driver/chromedriver.exe")
    browser = browsers.Chrome()
#     browser.capabilities = {"chromeOptions": {"args": ["--headless", "--disable-gpu"]}}
    
    async with get_session(service, browser) as session:
        await session.get(url)
        body = await session.get_page_source()
        links = await get_links(body)
        return links

async def get_links(html_str):
    
    html_r = HTML(html=html_str)
    laptop_links = [x for x in list(html_r.links) if x.startswith("https://rozetka.com.ua/")]

    datas = []
    for path in laptop_links:
        _id, _name = await extract_id(path)
        if _id:
            data = {
                "id":_id, 
                "name": _name,
                "path": path,
                "scraped": 0
            }
            datas.append(data)
    return datas

async def run(urls):
    links = []
    for url in urls:
        links.append(asyncio.create_task(scraper(url)))
    list_of_links = asyncio.gather(*links)
    return list_of_links

if __name__ == "__main__":
    url = 'https://rozetka.com.ua/notebooks/c80004/'
    loop = asyncio.get_event_loop()
#     results = loop.run_until_complete(scraper(url))
    results = asyncio.run(run(url))
