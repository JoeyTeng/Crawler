# mine_celeryconfig.py
# --coding:utf-8--

from default import PROJECT_NAME

# transport://userid:password@hostname:port/virtual_host
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# 0 = Retry forever. Default = 100
# BROKER_CONNECTION_MAX_RETRIES = 0

# To disable prefetching for fair distribution
# CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'rpc://'
# messages will not be lost after a broker restart if True
# CELERY_RESULT_PERSISTENT = False
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True
# tasks can be tracked before they are consumed by a worker.
CELERY_SEND_TASK_SENT_EVENT = True

# gzip, bzip2 (if available), or any registered in Kombuy.
CELERY_MESSAGE_COMPRESSION = 'gzip'
# Onlyif task is idempotent combine and that level of reliability is required.
CELERY_ACKS_LATE = True

CELERY_ROUTES = {"celery.ping": "default",
                 ("%s.mine.actor.mail" % PROJECT_NAME): {
                     "queue": "mine.mail",
                     "routing_key": "mine.mail"}
                 }
