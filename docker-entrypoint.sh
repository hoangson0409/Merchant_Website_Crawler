#!/bin/bash

set -e
if [ -f ".env_secret" ]; then
  crudini --merge .env < .env_secret
fi
dockerize -wait-retry-interval 3s -timeout 60s -wait tcp://${DB_HOST}:${DB_PORT}

WORKING_DIR=/django_project/scrapy_app/scrapy_app
LOG_FILE=$WORKING_DIR/logs/scrapyd.log

cd $WORKING_DIR
mkdir -p $WORKING_DIR/logs
nohup scrapyd > $LOG_FILE 2>&1 &
set +e
scrapyd-deploy scrapy_app -p ${PWSCRAPY_PROJECT}
set -e
sleep 3 && scrapyd-deploy scrapy_app -p ${PWSCRAPY_PROJECT}

cd /django_project
if [[ ( ! -z ${AUTO_MIGRATION+x} ) && ( "true" == "${AUTO_MIGRATION}" ) ]]; then
    echo "Executing migrations ..."
    python manage.py migrate
fi

exec "$@"
