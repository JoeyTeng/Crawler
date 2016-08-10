#interpreter.py
#--coding:utf-8--

import re

import celery

import wrapper
import default

PROJECT_NAME = default.PROJECT_NAME

interpreter = celery.Celery(main="interpreter", config_source='celeryconfig')

def url_on_failure_handler(exc, task_id, args, kwargs, einfo):
    pass

def get_domain(url):
    # Try to guess domain from url
    return re.search(r'(?<=://).+?(?:/.+?)?(?=[/$?])', ('%s/' %url)).group(0)

@interpreter.task(name=('%s.interpreter.url' %PROJECT_NAME),
                  ignore_result=True,
                  max_retries=3, # Default == 3
                  default_retry_delay=3*60) # Default == 3 * 60 second
def url(url, domain=None, parser=None):
    # parser: 'webpage' for bf4, 'rss' for feedparser
    url.on_failure = url_on_failure_handler # overwrite the function of instance
    domain = domain or get_domain(url)
    parser = parser or 'webpage'
    config = wrapper.wrap(url, domain)

    if parser == 'rss':
        interpreter.send_task(('%s.actor.rss' %PROJECT_NAME), args=config.args, kwargs=config.kwargs, routing_key='rss')
    elif parser == 'webpage':
        interpreter.send_task(('%s.actor.webpage' %PROJECT_NAME), args=config.args, kwargs=config.kwargs, routing_key='webpage')

@interpreter.task(name=('%s.interpreter.rss_failure' %PROJECT_NAME),
                  ignore_result=True,
                  max_retries=3,
                  default_retry_delay=3*60)
def rss_failure(exc=None, task_id=None, args=None, kwargs=None, einfo=None):
    pass

@interpreter.task(name=('%s.interpreter.webpage_failure' %PROJECT_NAME),
                  ignore_result=True,
                  max_retries=3,
                  default_retry_delay=3*60)
def webpage_failure(exc=None, task_id=None, args=None, kwargs=None, einfo=None):
    pass

if __name__ == '__main__':
    interpreter.start()
