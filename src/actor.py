#actor.py
#--coding:utf-8--

import celery

import downloader
import parser

import default

PROJECT_NAME = default.PROJECT_NAME

actor = celery.Celery(main='actor', config_source='celeryconfig')

_parser = parser # Name overwritten

def download(url, params=None, config=None, data='text'):
    return getattr(downloader.Downloader().get(url, params=params, config=config), data)

def parse(data, template=default.parser.template, config=default.parser.config, parser=None):
    for args, kwargs in _parser.parse(data, template=template, config=config, parser=parser): # should return (args, kwargs) which fits 'interpreter.url'
        actor.send_task(('%s.interpreter.url' %PROJECT_NAME), args=args, kwargs=kwargs, routing_key='url', queue='url')

def rss_on_failure_handler(exc, task_id, args, kwargs, einfo):
    pass

def webpage_on_failure_handler(exc, task_id, args, kwargs, einfo):
    pass

@actor.task(name=('%s.actor.rss' %PROJECT_NAME),
                  queue='rss',
                  ignore_result=True,
                  max_retries=3, # Default == 3
                  default_retry_delay=3*60) # Default == 3 * 60 second
def rss(url, downloader_config=None, parser_config=None):
    parse(download(url, params=downloader_config.params, config=downloader_config.config, data='content'),
              template=parser_config.template, config=parser_config.config, parser='rss')
    return True

@actor.task(name=('%s.actor.webpage' %PROJECT_NAME),
                  queue='webpage',
                  ignore_result=True,
                  max_retries=3,
                  default_retry_delay=3*60)
def webpage(url, downloader_config=None, parser_config=None):
    parse(download(url, params=downloader_config.params, config=downloader_config.config, data='content'),
                  template=parser_config.template, config=parser_config.config, parser='webpage')
    return True

if __name__ == '__main__':
    actor.start()
