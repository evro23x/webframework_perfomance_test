from datetime import datetime
import json
import asyncio

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient


def is_news_item_valid(news_item):
    return 'id' in news_item


async def test(request):
    return web.Response(text="Test")


async def add_news_handle(request):
    data = await request.json()

    if is_news_item_valid(data):
        data['date_added'] = datetime.now()
        result = await request.app['engine'].news.insert_one(data)
        return web.Response(text="Ok")
    else:
        return web.HTTPBadRequest(text="Id not found")


def app():
    _app = web.Application()
    _app['engine'] = AsyncIOMotorClient('mongodb://localhost:27017').db
    # _app['raven'] = raven.Client(settings.RAVEN_URL)
    _app.router.add_get('/', test)
    _app.router.add_post('/news/add', add_news_handle)
    return _app


if __name__ == "__main__":
    the_app = app()
    web.run_app(the_app, host='0.0.0.0', port=8000)
