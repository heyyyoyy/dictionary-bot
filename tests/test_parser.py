import pytest
import aresponses
import os
from app.async_parser import Scrapper
from bs4 import BeautifulSoup


class FakeScrapper(aresponses.ResponsesMockServer):

    async def __aenter__(self):
        await super().__aenter__()
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                  'data', 'last.html'))) as f:
            html = f.read()
        _response = self.Response(text=html, status=200, reason='OK')
        self.add(self.ANY, response=_response)


@pytest.yield_fixture(scope='session')
def scrapper():
    yield Scrapper('fake_request')


@pytest.yield_fixture(scope='session')
def html():
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
              'data/last.html'))) as f:
        yield f.read()


@pytest.yield_fixture(scope='session')
def soup(html):
    yield BeautifulSoup(html, 'lxml')


@pytest.mark.asyncio
async def test_get_html(scrapper, html, event_loop):
    async with FakeScrapper():
        html_ = await scrapper.get_html()
        assert html == html_


@pytest.mark.asyncio
async def test_get_title(scrapper, soup, event_loop):
    async with FakeScrapper():
        title = await scrapper.get_title(soup)
        assert title == 'last'
