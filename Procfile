cd src
unbuffer celery -A worker worker --loglevel=info >../celery.log 2>&1 &
python __main__.py
cd ..
