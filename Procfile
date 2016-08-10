export CURRENT_WORK_PATH=`pwd`
cd src
celery multi start interpreter -A interpreter.interpreter -Q url,rss_failure,webpage_failure -l debug --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid" --logfile="$CURRENT_WORK_PATH/tmp/celery/log/%n%I.log"
celery multi start actor -A actor.actor -Q rss,webpage -l debug --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid" --logfile="$CURRENT_WORK_PATH/tmp/celery/log/%n%I.log"
cd ..
