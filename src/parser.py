#parser.py
#--coding:utf-8--

import time

import feedparser

import default
import config
import store

class Parser(config.Config):

    def __call__(self, data=None, template=None, config=None, parser=None):
        if parser == "rss":
            for value in self.parse_rss(data, template=template, config=config):
                yield value
        elif parser == "webpage":
            for value in self.parse_webpage(data, template=template, config=config):
                yield value

    def release(self):
        # Ban the usage of release lock
        raise AttributeError("'%s' object has no attribute 'release'" %(__name__))

    @classmethod
    def parse_rss(cls, data, template=default.parser.template, config=default.parser.config):
        feedparsed = feedparser.parse(data)
        parsed = []
        for value in cls.extract(feedparsed, template):
            if type(value) == tuple:
                value = list(value)
                value.append({})
                try:
                    value[1]['domain'] = config.result.domain
                except:
                    pass
                try:
                    value[1]['parser'] = config.result.parser
                except:
                    pass

                yield tuple(value)
            else:
                parsed = value

        for data_parsed in parsed:
            store.save_data(data_parsed['_data'], _id=data_parsed['_id'], _time=data_parsed['_time'])

    @classmethod
    def parse_webpage(cls, data, template=default.parser.template, config=default.parser.config):
        yield data

    @classmethod
    def extract(cls, data, template):
        try:
            _store = template['_store']
            if _store == 'exclude':
                yield []

            _id = None
            _time = None

            _type = template['_type']
            result = []
            if _type == 'list':
                _data = []
                for element in data:
                    _result_pack = []
                    for value in cls.extract(element, template['_data']):
                        if type(_result_pack) == tuple:
                            yield _result_pack
                        else:
                            _result_pack = value

                    for _result in _result_pack:
                        if _store == 'pack':
                            _identity = False # If contains _id or _time
                            try: # Check for _id and _time
                                _id = _result['_id']
                                _identity = True
                            except:
                                pass
                            try:
                                _time = _result['_time']
                                _identity = True
                            except:
                                pass
                            if _identity:
                                _result = _result['_data']

                            if _result == None: # Remove 'id' and 'time'
                                continue

                        _data.append(_result)

                if _store == 'pack':
                    result = [_data]
                elif _store == 'unpack':
                    result = _data
            elif _type == 'dict':
                if _store == 'pack':
                    result = [{}]
                elif _store == 'unpack':
                    result = []

                for item in template.items():
                    if item[0][0] == '_' and item[0][1:].isalnum() and item[0] != '_data': # filter control/instruction items
                        continue

                    _result_pack = []
                    for value in cls.extract(data[item[0]], item[1]):
                        if type(_result_pack) == tuple:
                            yield _result_pack
                        else:
                            _result_pack = value

                    for _result in _result_pack: # To unpack the result
                        if _store == 'pack':
                            _identity = False # If contains _id or _time
                            try: #Check for _id and _time
                                _id = _result['_id']
                                _identity = True
                            except:
                                pass
                            try:
                                _time = _result['_time']
                                _identity = True
                            except:
                                pass
                            if _identity:
                                _result = _result['_data']

                            if _result != None: # Remove 'id' and 'time'
                                result[0][item[0]] = _result
                        elif _store == 'unpack':
                            result.append(_result)

            elif _type == 'data':
                result = [data]
            elif _type == 'url':
                result = [data]
                yield ([url],)
            elif _type == 'id':
                _id = data
                result = [None]
            elif _type == 'time':
                _time = time.mktime(data)
                result = [None]
            # Pack for special identity
            if _id != None or _time != None:
                result = {'_data': result[0]} # Unpack result to prevent double pack
                if _id != None:
                    result['_id'] = _id
                if _time != None:
                    result['_time'] = _time
                result = [result]

            yield result

        except KeyError:
            yield data

def parse(data, template=default.parser.template, config=default.parser.config, parser=None):
    for value in Parser(data=data, template=template, config=config, parser=parser):
        yield value

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

