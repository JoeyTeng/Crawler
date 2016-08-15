#wraper.py
#--coding:utf-8--

import json

import config
import default

class Wrapper(object):
    __slots__ = ('configs')
    def __init__(self, config_path):
        self.configs = json.load(open(config_path, 'rb'))

    def wrap(self, url, params, domain):
        _config = domain # iterative pointer
        try:
            while isinstance(_config, basestring): # Use pointer to compress data
                _config = self.configs[_config]
        except KeyError:
            return None

        _downloader_config = config.Config()
        _parser_config = config.Config()
        wrapped = config.Config()

        _downloader_config.params = params or _config.get('params')
        _downloader_config.config = _config.get('downloader_config')
        _parser_config.template = _config.get('template')
        _parser_config.config = (_config.get('parser_config') or config.Config())
        _parser_config_result = config.Config()
        _parser_config_result.domain = domain
        _parser_config_result.parser = 'webpage'
        _parser_config.config.result = (_parser_config.config.result or _parser_config_result)

        wrapped.args = [url]
        wrapped.kwargs = {'downloader_config': _downloader_config, 'parser_config': _parser_config}

        return wrapped

wrapper = Wrapper(default.CONFIG_PATH)

def wrap(url, params, domain):
    return wrapper.wrap(url, params, domain)

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")
