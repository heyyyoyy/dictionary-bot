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


# @pytest.yield_fixture(scope='session')
# def description():
#         with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
#               'data/desc_last.html'))) as f:
#         yield f.read()


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
    title = await scrapper.get_title(soup)
    assert title == 'last'


@pytest.yield_fixture()
@pytest.mark.asyncio
async def desc(scrapper, soup, event_loop):
    desc = await scrapper.get_descriptions(soup)
    yield desc


@pytest.mark.asyncio
async def test_get_translate(scrapper, desc, event_loop):
    translate = await scrapper.get_translate(desc[0])
    assert translate == 'последний'


@pytest.mark.asyncio
async def test_get_talking(scrapper, desc, event_loop):
    translate = await scrapper.get_talking(desc[0])
    assert translate == 'the most recent'


@pytest.mark.asyncio
async def test_get_example(scrapper, desc, event_loop):
    translate = await scrapper.get_example(desc[0])
    assert translate == 'What was the last film you saw?'


@pytest.mark.asyncio
async def test_run(scrapper, event_loop):
    async with FakeScrapper():
        result = await scrapper.run()
        assert result == ('last\nthe most recent\nпоследний\n'
                          'What was the last film you saw?\n'
                          'The last book, house, job, etc is the one '
                          'before the present one.\nпредыдущий, прошлый\n'
                          'I liked his last book but I\'m not so keen on this'
                          ' one.\nhappening or coming at the end\n'
                          'последний\nIt\'s the last room on the left.\n'
                          'only remaining\nпоследний, оставшийся\n'
                          'Who wants the last piece of cake?\n'
                          'the least expected or wanted person or thing\n'
                          'самый неподходящий или неожиданный человек/предмет'
                          ' и т. д.\nThree extra people to feed - that\'s '
                          'the last thing I need!')
