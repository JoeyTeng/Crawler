#task_loader.py
#--coding:utf-8--

import json

import celery

import default

PROJECT_NAME = default.PROJECT_NAME

task_loader = celery.Celery(main="task_loader", config_source='celeryconfig')

def load(url, params=None, domain=None, parser=None):
    args = [url]
    kwargs = {'params': params, 'domain': domain, 'parser': parser}
    task_loader.send_task(('%s.interpreter.url' %PROJECT_NAME), args=args, kwargs=kwargs, routing_key='url', queue='url')

def main(task_path):
    tasks = json.load(open(task_path, 'rb'))
    for task in tasks:
        load(task['url'], task.get('params'), task.get('domain'), task.get('parser'))

if __name__ == '__main__':
    main(default.TASK_PATH)
