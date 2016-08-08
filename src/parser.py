#parser.py
#--coding:utf-8--

import feedparser

import default
import config
import store

class Parser(config.Config):

    def __init__(self, data=None, template=None, config=None):
        pass

    def release(self):
        # Ban the usage of release lock
        raise AttributeError("'%s' object has no attribute 'release'" %(__name__))

    @classmethod
    def parse(cls, data, template=default.parser.template, config=default.parser.config):
        feedparsed = feedparser.parse(data)
        parsed = cls.extract(feedparsed, template)
        return parsed
        store.save_data(parsed)
        return True

    @classmethod
    def extract(cls, data, template):
        try:
            _type = template['_type']
            result = {}
            if _type == 'list':
                result = {}
                result['_type'] = 'list'
                _data = []
                for element in data:
                    _data.append(cls.extract(element, template['_data']))
                result['_data'] = _data
            elif _type == 'data':
                result = data
            elif _type == 'dict':
                result = {}
                for item in template.items():
                    if item[0][0] == '_' and item[0][1:].isalnum() and item[0] != '_data': # filter control/instruction items
                        continue
                    result[item[0]] = cls.extract(data[item[0]], item[1])
            elif _type == 'id':
                result = {'_data': data, '_type': 'id'}
            elif _type == 'time':
                result = {'_data': data, '_type': 'time'}

            return result

        except KeyError:
            return data

def parse(data, template=default.parser.template, config=default.parser.config):
    return Parser.parse(data=data, template=template, config=config)

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

