# store.py
# --coding:utf-8--

import time
import pymongo

import syntactic_sugar
import default

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

# Protect by code above

config = default.store

MONGO_CONN = pymongo.MongoClient(config.host, config.port)


def save_data(data, _id=None, _time=None, collection=None, database=None):
    if _id is None:
        data['_id'] = data['_id']
        _id = data['_id']
    if _time is None:
        gmt = time.gmtime()
        data['UpdateTime'] = time.asctime(gmt)

    collection = collection or config.collection
    database = database or config.database

    # UTC time in s since Epoch
    _timestamp = _time or data.get('_timestamp') or (time.time(
    ) + (time.altzone if time.daylight else time.timezone))
    data['_timestamp'] = _timestamp

    with syntactic_sugar.suppress(pymongo.errors.DuplicateKeyError):
        MONGO_CONN[database][collection].update_one(
            filter={'_id': _id, '_timestamp': {'$lt': _timestamp}},
            update={'$set': data},
            upsert=True)
