import json

from meinheld import server
import motor.motor_asyncio
from pymongo import MongoClient


def get_mongo_connector(is_async=False, db_url='mongodb://localhost:27017'):
    if is_async:
        return motor.motor_asyncio.AsyncIOMotorClient(db_url).db
    else:
        return MongoClient(db_url).db


def is_news_item_valid(news_item):
    return 'id' in news_item


def add_news_item_to_db(news_item):
    get_mongo_connector(is_async=True).news.insert_one(news_item)


def add_news_handle(environ):
    news_item = json.loads(environ["wsgi.input"].read().decode('utf-8'))
    if is_news_item_valid(news_item):
        add_news_item_to_db(news_item)
        status, res = '200 OK', b''
    else:
        status, res = '400 OK', b'bad data'
    return status, res


def dispatch(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/news/add':
        status, res = add_news_handle(environ)
    else:
        status, res = '404 Not Found', b'not found'
    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(res)))]
    start_response(status, response_headers)
    return [res]


if __name__ == '__main__':
    server.listen(("0.0.0.0", 8000))
    server.run(dispatch)
