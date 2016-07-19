#worker.py
#--coding:utf-8--

import celery

import downloader 
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
def Crawler(url, parms=None, config=None, data='text'):
    return getattr(downloader.Downloader().get(url, parms=parms, config=conifg), data)

