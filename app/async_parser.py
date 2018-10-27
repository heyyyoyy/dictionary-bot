from bs4 import BeautifulSoup
from aiohttp import ClientSession


class Scrapper:

    __slots__ = 'world', 'url', 'header'

    def __init__(self, world):
        self.url = ('https://dictionary.cambridge.org/dictionary/english-'
                    'russian/')
        self.world = world
        self.header = {'User-Agent': ('Mozilla/5.0'
                                      '(X11;Linux x86_64) AppleWebKit/537.36'
                                      ' (KHTML, like Gecko)'
                                      'Chrome/68.0.3440.75 Safari/537.36')}

    async def get_html(self):
        async with ClientSession() as session:
            async with session.get(self.url + self.world,
                                   headers=self.header) as resp:
                return await resp.text()

    async def get_title(self, html):
        return html.find('div', class_='h3 di-title cdo-section-title-hw').text

    async def get_descriptions(self, html):
        return html.find_all('div', class_='def-block pad-indent')

    async def get_talking(self, desc):
        return desc.find('b', class_='def').text.strip()

    async def get_translate(self, desc):
        return desc.find('span', class_='trans').text.strip()

    async def get_example(self, desc):
        ex = desc.find('span', class_='eg')
        if ex is not None:
            return ex.text.strip()
        return ''

    async def run(self):
        html_ = await self.get_html()
        html = BeautifulSoup(html_, 'lxml')
        content = []
        title = await self.get_title(html)
        content.append(title)
        descriptions = await self.get_descriptions(html)
        for d in descriptions:
            talking = await self.get_talking(d)
            transl = await self.get_translate(d)
            ex = await self.get_example(d)
            content.extend([talking, transl, ex])
        return '\n'.join(content)
