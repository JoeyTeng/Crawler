# mine_actor.py
# --coding:utf-8--
# Connect with all the plugins that processing the data from miner.

import celery

import default
import config

import mail

PROJECT_NAME = default.PROJECT_NAME

mine_actor = celery.Celery(
    main='mine_actor', config_source='mine_celeryconfig')


@mine_actor.task(name=('%s.mine.actor.mail' % PROJECT_NAME),
                 queue='mine.mail',
                 ignore_result=True,
                 max_retries=3,  # Default == 3
                 default_retry_delay=3 * 60)  # Default == 3 * 60 second
def mail_notify(content, send_config=None):
    _config = config.Config(send_config or {})  # config.Config(None) is False

    mail.send(content, _config)

    return True

if __name__ == '__main__':
    mine_actor.start()
