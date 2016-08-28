#!/bin/bash
showopts () {
  while getopts ":pq:" optname
    do
      case "$optname" in
        "p")
          echo "Option $optname is specified"
          ;;
        "q")
          echo "Option $optname has value $OPTARG"
          ;;
        "?")
          echo "Unknown option $OPTARG"
          ;;
        ":")
          echo "No argument value for option $OPTARG"
          ;;
        *)
        # Should not occur
          echo "Unknown error while processing options"
          ;;
      esac
    done
  return $OPTIND
}

showargs () {
  for p in "$@"
    do
      echo "[$p]"
    done
}

optinfo=$(showopts "$@")
argstart=$?
arginfo=$(showargs "${@:$argstart}")

CURRENT_WORK_PATH=`pwd`
mkdir -p "$CURRENT_WORK_PATH/tmp/celery/run"
mkdir -p "$CURRENT_WORK_PATH/tmp/celery/log"
arg="$1"
cd src

if [[ "$arg" == "" || "$arg" == "help" ]]
then
    echo "options: start, restart, stop"
elif [ $arg == "start" ]
then
    celery multi start interpreter -A interpreter.interpreter -Q url,rss_failure,webpage_failure -l debug --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid" --logfile="$CURRENT_WORK_PATH/tmp/celery/log/%n%I.log"
    celery multi start actor -A actor.actor -Q rss,webpage -l debug --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid" --logfile="$CURRENT_WORK_PATH/tmp/celery/log/%n%I.log"
elif [ $arg == "restart" ]
then
    celery multi restart interpreter -A interpreter.interpreter -Q url,rss_failure,webpage_failure -l debug --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid" --logfile="$CURRENT_WORK_PATH/tmp/celery/log/%n%I.log"
    celery multi restart actor -A actor.actor -Q rss,webpage -l debug --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid" --logfile="$CURRENT_WORK_PATH/tmp/celery/log/%n%I.log"
elif [ $arg == "stop" ]
then
    celery multi stopwait interpreter --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid"
    celery multi stopwait actor --pidfile="$CURRENT_WORK_PATH/tmp/celery/run/%n.pid"
fi

cd ..
