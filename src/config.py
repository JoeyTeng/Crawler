#config.py
#--coding:utf-8--

class Config(object):
    __slots__ = ('_attr', '_lock')

    def __init__(self):
        self._attr = dict()
        self._lock = False

    def lock(self):
        self._lock = True

    def release(self):
        self._lock = False

    def __getattr__(self, attr):
        if attr in self.__attr:
            return self.__attr[attr]
        else:
            if self._lock:
                return None

            self.__attr[attr] = None
            return self.__attr[attr]

    def __delattr__(self, attr):
        try:
            self.__attr.pop(attr)
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" %(__name__, attr))

    def del_attr(self, attr):
        self.__delattr__(attr)

class Downloader(Config):
    pass

