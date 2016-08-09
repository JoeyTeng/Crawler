#store.py
#--coding:utf-8--

import time
import pymongo

import default

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

# Protect by code above

config = default.store

MONGO_CONN = pymongo.MongoClient(config.host, config.port)

def save_data(data, _id=None, _time=None, collection=None):
    if _id == None:
        data['_id'] = data['_id']
        _id = data['_id']
    if _time == None:
        gmt = time.gmtime()
        data['UpdateTime'] = time.asctime(gmt)
        _time = time.mktime(gmt)
    if collection == None:
        collection = config.collection

    MONGO_CONN[config.database][collection].update_one(
            filter={'_id': _id},
            update={'$set': data},
            upsert=True
    )
