from datetime import datetime
import json
import asyncio

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient


async def is_news_item_valid(news_item, engine):
    real_result = 'id' in news_item and not await engine.news.find({'id': news_item['id']}).count()
    return True


async def test(request):
    return web.Response(text="Test")


async def add_news_handle(request):
    data = await request.json()

    is_valid = await is_news_item_valid(data, request.app['engine'])
    if is_valid:
        data['date_added'] = datetime.now()
        result = request.app['engine'].news.insert_one(data)
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


APP = app()

if __name__ == "__main__":
    web.run_app(APP, host='0.0.0.0', port=8000)
