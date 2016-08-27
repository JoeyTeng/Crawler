# config.py
# --coding:utf-8--


class Config(object):
    __slots__ = ('__dict__')

    def __init__(self, data=None):
        data = data or {}
        for item in data.iteritems():
            if isinstance(item[1], dict):
                self.__dict__[item[0]] = self.__class__(
                    item[1])  # Rebuilt config from a dict object
            else:
                self.__dict__[item[0]] = item[1]

    def __str__(self):
        return ("%r" % (self.__dict__))

    def __unicode__(self):
        return unicode(self.__str__)

    def __repr__(self):
        return "%r: %s" % (id(self), self.__str__())

    def __getitem__(self, y):
        item = self.__dict__.__getitem__(y)
        if isinstance(item, dict):
            item = self.__class__(item)
        if isinstance(item, self.__class__):
            return dict(item)
        else:
            return item

    def __iter__(self):
        for item in self.__dict__.iteritems():
            # print isinstance(item[1], self.__class__)
            value = item[1]
            if isinstance(value, dict):
                value = self.__class__(value)
            if isinstance(value, self.__class__):
                for item_ in value:
                    print type(item_)
                    yield item_
            else:
                yield item

    def __len__(self):
        return self.__dict__.__len__()

    def copy(self):
        return self.__dict__.copy()

    def get(self, k, d=None):
        return self.__dict__.get(k, d)

    def items(self):
        return self.__dict__.items()

    def iteritems(self):
        return self.__dict__.iteritems()

    def iterkeys(self):
        return self.__dict__.iterkeys()

    def keys(self):
        return self.__dict__.keys()

    def __getattr__(self, name, default=None):
        if name == 'read':
            raise AttributeError(
                "'%s' object has no attribtue 'read' (adapting for requests module)" % (__name__))
        return self.get(name, default)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __delattr__(self, name):
        try:
            self.__dict__.pop(name)
        except KeyError:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (__name__, name))

    def del_attr(self, name):
        self.__delattr__(name)


class Downloader(Config):
    pass
