import json
from __init__ import config
from __init__ import worker

configs = json.load(open('config.json', 'rb'))
parsed = []


downloader_config = config.Config()
parser_config = config.Config()

def test(config):
    #print downloader_config.__getattr__('params')
    downloader_config.params = config['params']
    downloader_config.config = None
    parser_config.template = config['template']
    parser_config.config = None
    url = config['url']
    return worker.crawler(url, downloader_config=downloader_config, parser_config=parser_config)

for config in configs:
    parsed.append(test(config))
