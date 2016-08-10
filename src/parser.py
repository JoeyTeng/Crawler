#parser.py
#--coding:utf-8--

from bs4 import BeautifulSoup

import default
import config

class Parser(config.Config):

    def __call__(self, data=None, template=None, config=None):
        if data == None:
            raise ValueError("Do Not Call This Class Without Input")

        for value in self.parse(data, template=template, config=config):
            yield value

    def release(self):
        # Ban the usage of release lock
        raise AttributeError("'%s' object has no attribute 'release'" %(__name__))

    def parse(data, template=default.parser.template, config=default.parser.config):
        yield data

def parse(data, template=default.parser.template, config=default.parser.config):
    for value in Parser(data=data, template=template, config=config):
        yield value

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

