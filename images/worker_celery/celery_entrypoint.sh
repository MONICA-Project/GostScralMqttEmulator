#!/bin/sh

echo "CELERY ENTRYPOINT 1"

# wait for RabbitMQ server to start
sleep 10

echo "CELERY ENTRYPOINT 2"

cd worker

echo "CELERY ENTRYPOINT 3"

# FIXME: Retrieved from web container (DB Migration)
# prepare init migration
su -m myuser -c "python manage.py makemigrations users jobs shared --settings=shared.settings.appglobalconf"
# migrate db, so we have the latest db schema
su -m myuser -c "python manage.py migrate --settings=shared.settings.appglobalconf"
# FIXME: Retrieved from web (DB Migration)

echo "CELERY ENTRYPOINT 4"

chown myuser:myuser ./jobs
chown myuser:myuser ./manage.py

echo "CELERY ENTRYPOINT 5"

sleep 15

# run Celery worker for our project monica with Celery configuration stored in Celeryconf
#su -m myuser -c "celery -A jobs.tasks worker -Q priority_queue,crowd_queue_elaboration, queue_sw_update_info --loglevel=debug -n worker1@%h -c 50 -B"
#su -m myuser -c "celery -A jobs.broker_connection worker -Q broker_queue --loglevel=info -n worker2@%h"
su -m myuser -c "celery -A jobs.tasks worker -Q priority_queue,taskqueue_provisioning,queue_sw_update_info,queue_task_alive --without-mingle --loglevel=warning -c 10 -B"

echo "CELERY ENTRYPOINT 6"
