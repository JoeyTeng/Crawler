#default.py
#--coding:utf-8--

PROJECT_NAME = 'crawler'
CONFIG_PATH = 'config.json'
TASK_PATH = 'primer.json'

class downloader(object):
    __slots__ = ()
    params = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    allow_redirects = True
    timeout = 3 # 3 seconds
    proxies = None

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")

class parser(object):
    __slots__ = ()
    template = None
    config = None

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Module")
