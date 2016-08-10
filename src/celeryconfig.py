#celeryconfig.py
#--coding:utf-8--

# transport://userid:password@hostname:port/virtual_host
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# 0 = Retry forever. Default = 100
# BROKER_CONNECTION_MAX_RETRIES = 0

# To disable prefetching for fair distribution
# CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_RESULT_SERIALIZER = 'pickle'
# CELERY_RESULT_BACKEND = 'rpc://'
# messages will not be lost after a broker restart if True
# CELERY_RESULT_PERSISTENT = False
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True

# gzip, bzip2 (if available), or any registered in Kombuy.
CELERY_MESSAGE_COMPRESSION = 'gzip'
# Onlyif task is idempotent combine and that level of reliability is required.
CELERY_ACKS_LATE = True

CELERY_ROUTES = {"celery.ping": "default",
                 "actor.rss" : {
                     "queue": "rss",
                     "routing_key": "rss"},
                 "actor.webpage": {
                     "queue": "webpage",
                     "routing_key": "webpage"},
                 "interpreter.rss_failure": {
                     "queue": "rss_failure",
                     "routing_key": "rss_failure"},
                 "interpreter.webpage_failure": {
                     "queue": "webpage_failure",
                     "routing_key": "webpage_failure"},
                 "interpreter.url": {
                     "queue": "url",
                     "routing_key": "url"}}

