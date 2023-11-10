import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from lxml import etree

class ScraperPool(object):
    def __init__(self, urls, headers):
        self.urls = urls
        self.headers = headers
        self.result_data  = []
        asyncio.run(self.main())

    async def fetch(self, semaphore, session, url):
        async with semaphore:
            try:
                async with session.get(url) as response:
                    html = await response.text()
                    return url, html
            except Exception as e:
                print(str(e))

    async def main(self):
        tasks = []
        semaphore = asyncio.Semaphore(10)

        async with aiohttp.ClientSession(headers=self.headers) as session:
            
            for url in self.urls:
                tasks.append(self.fetch(semaphore, session, url))

            htmls = await asyncio.gather(*tasks)
            self.result_data.extend(htmls)

class ScraperEngine:

    def __init__(self, urls, headers, elements) -> None:
        self.urls = urls
        self.headers = headers
        self.elements = elements

    def scrape(self) -> dict:
        result_json_dict = {}

        scraper_results = ScraperPool(self.urls, self.headers).result_data

        for result in scraper_results:
            soup = BeautifulSoup(result[1], 'html.parser')
            dom = etree.HTML(str(soup))
            url_result = {}
            for el in self.elements:
                xpath_res = dom.xpath(el['xpath'])
                if ('regex_sub_pattern' in el.keys()) and ('regex_sub_repl' in el.keys()):
                    if len(el['regex_sub_pattern']) > 0:
                        for i, res in enumerate(xpath_res):
                            xpath_res[i] = re.sub(el['regex_sub_pattern'], el['regex_sub_repl'], res)
                if ('regex_search' in el.keys()) and (len(el['regex_search']) > 0):
                    for i, res in enumerate(xpath_res):
                        match = re.search(el['regex_search'], res)
                        if match:
                            xpath_res[i] = match.group()
                if ('concat_results' in el.keys()) and (len(el['concat_results']) > 0):
                    xpath_res = el['concat_results'].join(xpath_res)
                if len(xpath_res) == 1:
                    xpath_res = xpath_res[0]
                url_result[el['name']] = xpath_res
            result_json_dict[result[0]] = url_result

        return result_json_dict
