#downloader.py
#--coding:utf-8--

import requests

import default

class Downloader(object):
    __slots__ = ('_config')

    def __init__(self, config=default.downloader):
        self._config = config

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

        return self

    def get(self, url, params=None, config=None):
        if params == None:
            params = self._config.params
        if config == None:
            config = self._config

        self._req = requests.get(url, params=params, headers=config.headers, 
                allow_redirects=config.allow_redirects, timeout=config.timeout,
                proxies=config.proxies)

        return self

    @property
    def encoding(self):
        try:
            return self._req.encoding
        except AttributeError:
            return None

    @property
    def headers(self):
        try:
            return self._req.headers
        except AttributeError:
            return None

    @property
    def cookies(self):
        try:
            return self._req.cookies
        except AttributeError:
            return None

    @property
    def text(self):
        try:
            return self._req.text
        except AttributeError:
            return None

    @property
    def content(self):
        try:
            return self._req.content
        except AttributeError:
            return None

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Module")
