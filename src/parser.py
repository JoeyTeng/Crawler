#parser.py
#--coding:utf-8--

import BeautifulSoup

import default
import config

class Parser(Config.config):

    def __init__(self, data=None, template=None, config=None):
        if data == None:
            raise ValueError("Do Not Initialize This Class Without Input")

        self.parse(data, template=template, config=config)

    def release(self):
        # Ban the usage of release lock
        raise AttributeError("'%s' object has no attribute 'release'" %(__name__))

    def parse(data, template=default.parser.template, config=default.parser.config):
        return data

def parse(data, template=default.parser.template, config=default.parser.config):
    return Parser(data=data, template=template, config=config)

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

