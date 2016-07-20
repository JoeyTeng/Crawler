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

@app.task
def crawler(url, downloader_config=default.downloader, parser_config=default.parser):
    return parser(downloader(url, parms=downloader_config.parms, config=downloader_config.config),
            template=parser_config.parser.template, config=parser_config.parser.config)

def downloader(url, parms=None, config=None, data='text'):
    return getattr(downloader.Downloader().get(url, parms=parms, config=conifg), data)

def parser(data, template=default.parser.template, config=default.parser.config):
    return parser.parse(data, template=template, config=config)
