#store.py
#--coding:utf-8--

import datetime
import pymongo

import default

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

# Protect by code above

config = default.store

MONGO_CONN = pymongo.MongoClient(config.host, config.port)

def save_data(url, data):
    data['_id'] = data['url']
    data['UpdateTime'] = datetime.datetime.isoformat(datetime.datetime.now())

    MONGO_CONN[config.database][config.database.collection].update_one(
            filter={'_id': data['_id']},
            update={'$set': data},
            upsert=True
    )
