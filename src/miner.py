# miner.py
import re
import sys
import json
import time

import celery
import pymongo

import config
import default
import syntactic_sugar

PROJECT_NAME = default.PROJECT_NAME


class Miner(object):

    def __init__(self, _config=None):
        self._config = config.Config(_config or default.miner.config)

        self.celery_connection = celery.Celery(
            main='miner', config_source='mine_celeryconfig')

        self.mongo_config = default.store
        self.mongo_connection = pymongo.MongoClient(
            self.mongo_config.host, self.mongo_config.port)

        self._cursor = None
        self._collection = None
        self._lower_time = None
        self._upper_time = None

    def _find(self, collection, filter, cursor_type=None, sort=None):
        return self.mongo_connection[self.mongo_config.database][collection].find(filter=filter, cursor_type=cursor_type, sort=sort)

    def _find_one(self, collection, filter):
        return self.mongo_connection[self.mongo_config.database][collection].find_one(filter=filter)

    def _set_one(self, collection, filter, data, upsert=True):  # using $set
        self.mongo_connection[self.mongo_config.database][collection].update_one(
            filter=filter, update={'$set': data}, upsert=upsert)

    def cursor(self, **kwargs):
        """ kwargs:
            * collection: collection in db
            * lower_time: documents with _timestamp $gte lower_time
            * upper_time: documents with _timestamp $lt upper_time
        """
        collection = kwargs.get('collection')
        lower_time = kwargs.get('lower_time')
        upper_time = kwargs.get('upper_time')

        if collection or lower_time or upper_time:
            try:
                self._collection = collection or self._collection
                self._lower_time = lower_time or self._lower_time
                self._upper_time = upper_time or self._upper_time
            except NameError:
                raise RuntimeError("Use cursor without initialization")

            self._cursor = self._find(collection=collection,
                                      filter={'_timestamp': {
                                          '$gte': lower_time, '$lt': upper_time}},
                                      cursor_type=pymongo.cursor.CursorType.EXHAUST,
                                      sort=[('_timestamp', pymongo.ASCENDING)])

        else:
            return self._cursor

        return self._cursor

    def mine(self):
        for collection in self._config.collections:
            _lower_time = None
            with syntactic_sugar.suppress(TypeError):
                _lower_time = self._find_one(
                    collection, {'_id': 'Checked Time'})['time']
            _lower_time = _lower_time or float(-1)
            # UTC time in s since Epoch
            _upper_time = time.time() + (time.altzone if time.daylight else time.timezone)

            for document in self.cursor(collection=collection, lower_time=_lower_time, upper_time=_upper_time):
                self.route(collection, document)

        self._set_one(collection, {'_id': 'Checked Time'}, {'_id': 'Checked Time', 'time': _upper_time})

    def route(self, collection, document):
        for routing_keys, rules, mode, addressee in self._config.route[collection]:
            if mode.lower() == 'and':
                for field, pattern in rules:
                    if re.search(pattern, document[field]) is None:
                        break
                else:  # Execute only when exit loop normally (No break)
                    self.publish(routing_keys, self.compile_message(
                        collection, document, routing_keys, field, addressee))
            elif mode.lower() == 'or':
                for field, pattern in rules:
                    if re.search(pattern, document[field]) is not None:
                        self.publish(routing_keys, self.compile_message(
                            collection, document, routing_keys, field, addressee))
                        break

    def compile_message(self, collection, document, *args):
        routing_keys, field, addressee = args

        return {'routing_keys': routing_keys, 'content': document[field], 'addressee': addressee}

    def publish(self, routing_keys, data):
        for routing_key in routing_keys:
            routing_key = self._config.publish.routing_key[routing_key]
            self.celery_connection.send_task(('%s.mine.actor.mail' % PROJECT_NAME),
                                             args=[data], kwargs={}, routing_key=routing_key)

    def start(self):
        self.mine()

if __name__ == '__main__':
    _config = None
    with syntactic_sugar.suppress(IndexError):
        _config = json.load(open(sys.argv[1]))
    _config = _config or default.miner.config or json.load(
        open(default.miner.config_path, 'rb'))

    Miner(_config).start()
