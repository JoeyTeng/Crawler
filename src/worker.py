#worker.py
#--coding:utf-8--

import celery

import downloader
import parser

import default

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")

# Protect by code above

WORKER_NAME = default.worker.worker_name
BROKER = default.worker.broker
BACKEND = default.worker.backend
PERSISTENT = default.worker.persistent

app = celery.Celery(WORKER_NAME, broker=BROKER, backend=BACKEND, persistent=PERSISTENT)

def download(url, params=None, config=None, data='text'):
    return getattr(downloader.Downloader().get(url, params=params, config=config), data)

def parse(data, template=default.parser.template, config=default.parser.config):
    return parser.parse(data, template=template, config=config)

@app.task
def crawler(url, downloader_config=default.downloader, parser_config=default.parser):
    return parse(download(url, params=downloader_config.params, config=downloader_config.config, data='content'),
            template=parser_config.template, config=parser_config.config)
