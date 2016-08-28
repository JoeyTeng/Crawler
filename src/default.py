# default.py
# --coding:utf-8--

import json

import config

PROJECT_NAME = 'crawler'
CONFIG_PATH = 'config.json'
TASK_PATH = 'primer.json'


class store(object):
    __slots__ = ()
    host = 'localhost'
    port = 27017
    database = 'crawler_FIA_test'
    collection = 'test'

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")


class downloader(object):
    __slots__ = ()
    params = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    allow_redirects = True
    timeout = 3  # 3 seconds
    proxies = None

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")


class parser(object):
    __slots__ = ()
    template = None
    config = None

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")


class miner(object):
    __slots__ = ()
    config_path = 'mine_config.json'
    config = config.Config(json.load(open(config_path, 'rb')))

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")


class mail(object):
    __slots__ = ()
    config_path = 'mail_config.json'
    config = config.Config(json.load(open(config_path, 'rb')))

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Module")
