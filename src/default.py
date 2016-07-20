#default.py
#--coding:utf-8--

class downloader(object):
    __slots__ = ()
    parms = None
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

class worker(object):
    __slots__ = ()
    worker_name = 'worker'
    broker = 'amqp://guest@localhost//'
    backend = 'rpc://'
    persistent = False # Result is transient

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")

class task(object):
    __slots__ = ()
    downloader = downloader
    parser = parser
    url = ""

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")

class manager(object):
    __slots__ = ()
    task = task

    def __init__(self):
        raise AttributeError("Do Not Instantiate This Class")

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Module")
