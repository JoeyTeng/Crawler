# parser.py
# --coding:utf-8--

import time

import feedparser

import syntactic_sugar
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

    @classmethod
    def parse_rss(cls, data, template=default.parser.template, config=default.parser.config):
        feedparsed = feedparser.parse(data)
        parsed = []
        for value in cls.extract(feedparsed, template):
            if type(value) == tuple:
                value = list(value)
                value.append({})
                with syntactic_sugar.suppress(TypeError, KeyError):
                    value[1]['domain'] = config.result.domain
                with syntactic_sugar.suppress(TypeError, KeyError):
                    value[1]['parser'] = config.result.parser

                yield tuple(value)
            else:
                parsed = value

        for data_parsed in parsed:
            store.save_data(data_parsed['_data'], _id=data_parsed[
                            '_id'], _time=data_parsed['_time'], collection='rss')

    @classmethod
    def parse_webpage(cls, data, template=default.parser.template, config=default.parser.config):
        _data = {'data': data, '_id': id(data)}
        store.save_data(_data, _id=_data['_id'], collection='webpage')
        return  # To prevent yield NoneType
        yield  # To make a generator

    @classmethod
    def extract(cls, data, template):
        try:
            _store = template['_store']
            if _store == 'exclude':
                yield []
                return

            _id = None
            _time = None

            _type = template['_type']
            result = []
            if _type == 'list':
                _data = []
                for element in data:
                    _result_pack = []
                    for value in cls.extract(element, template['_data']):
                        if type(value) == tuple:
                            yield value
                        else:
                            _result_pack = value

                    for _result in _result_pack:
                        if _store == 'pack':
                            _identity = False  # If contains _id or _time
                            # Check for _id and _time
                            with syntactic_sugar.suppress(TypeError, KeyError):
                                _id = _result['_id']
                                _identity = True
                            with syntactic_sugar.suppress(TypeError, KeyError):
                                _time = _result['_time']
                                _identity = True

                            if _identity:
                                _result = _result['_data']

                            if _result is None:  # Remove 'id' and 'time'
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
                    # filter control/instruction items
                    if item[0][0] == '_' and item[0][1:].isalnum() and item[0] != '_data':
                        continue

                    _result_pack = []
                    for value in cls.extract(data[item[0]], item[1]):
                        if type(value) == tuple:
                            yield value
                        else:
                            _result_pack = value

                    for _result in _result_pack:  # To unpack the result
                        if _store == 'pack':
                            _identity = False  # If contains _id or _time
                            # Check for _id and _time
                            with syntactic_sugar.suppress(TypeError, KeyError):
                                _id = _result['_id']
                                _identity = True
                            with syntactic_sugar.suppress(TypeError, KeyError):
                                _time = _result['_time']
                                _identity = True

                            if _identity:
                                _result = _result['_data']

                            if _result is not None:  # Remove 'id' and 'time'
                                result[0][item[0]] = _result
                        elif _store == 'unpack':
                            result.append(_result)

            elif _type == 'data':
                result = [data]
            elif _type == 'url':
                result = [data]
                yield ([data],)
            elif _type == 'id':
                _id = data
                result = [None]
            elif _type == 'time':
                _time = time.mktime(data)
                result = [None]
            # Pack for special identity
            if _id is not None or _time is not None:
                # Unpack result to prevent double pack
                result = {'_data': result[0]}
                if _id is not None:
                    result['_id'] = _id
                if _time is not None:
                    result['_time'] = _time
                result = [result]

            yield result

        except KeyError:
            yield data


def parse(data, template=default.parser.template, config=default.parser.config, parser=None):
    for value in Parser()(data=data, template=template, config=config, parser=parser):
        yield value

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")
