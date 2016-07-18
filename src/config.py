#config.py
#--coding:utf-8--

class Config(object):

    def __init__(self):
        self._attr = dict()

    def __getattr__(self, attr):
        if attr in self.__attr:
            return self.__attr[attr]
        else:
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

