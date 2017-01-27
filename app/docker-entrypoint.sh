#!/bin/bash

function check_db {
  python check_db.py
}

count=0
until ( check_db )
do
  ((count++))
  if [ ${count} -gt 10 ]
  then
    echo "ERROR: Services didn't become ready in time"
    exit 1
  fi
  sleep 1
done

python django/manage.py migrate                  # Apply database migrations
python django/manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
LOGFILE=/logs/gunicorn.log
ERRORFILE=/logs/gunicorn-error.log
ACCESSFILE=/logs/gunicorn-access.log

touch $LOGFILE
touch $ERRORFILE
touch $ACCESSFILE

tail -n 0 -f /logs/*.log &

GUNICORN_CONF=/app/gunicorn_conf.py

# Start Gunicorn processes
echo Starting Gunicorn.

exec gunicorn herd.wsgi:application \
    -c $GUNICORN_CONF \
    --chdir django \
    --name herd \
    --bind 0.0.0.0:8000 \
    --log-level=debug \
    --timeout 90 \
    --log-file=$LOGFILE 2>>$LOGFILE 1>>$ERRORFILE \
    --access-logfile=$ACCESSFILE \
    "$@"