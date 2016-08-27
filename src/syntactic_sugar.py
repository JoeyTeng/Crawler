# syntactic_suger.py
# --coding:utf-8--
# Some functions make the code stylish

import contextlib


@contextlib.contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass
