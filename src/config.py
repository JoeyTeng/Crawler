#config.py
#--coding:utf-8--

class Config(object):
    __slots__ = ('_lock', '__dict__')

    def __init__(self):
        self.__dict__['_lock'] = False # To avoid check __getattr__() and for uniform rule

    def lock(self):
        self._lock = True

    def release(self):
        self._lock = False

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" %(__name__, name))

    def __setattr__(self, name, value):
        if self._lock and (not self.__dict__.has_key(name)):
            raise AttributeError("'%s' object is locked" %(__name__))
        else:
            self.__dict__[name] = value

    def __delattr__(self, name):
        try:
            self.__dict__.pop(name)
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" %(__name__, name))

    def del_attr(self, name):
        self.__delattr__(name)

class Downloader(Config):
    pass

