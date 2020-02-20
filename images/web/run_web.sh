#!/bin/sh

# wait for PSQL server to start
sleep 10

cd worker

# su -m myuser -c "[ ! -d logs ] && mkdir logs"

# prepare init migration
# su -m myuser -c "python manage.py makemigrations users jobs shared --settings=shared.settings.appglobalconf"
# migrate db, so we have the latest db schema
# su -m myuser -c "python manage.py migrate --settings=shared.settings.appglobalconf"
# create superuser
#su -m myuser -c "python manage.py createsuperuser --settings=project.settings.local"  # username: demo    -     password: ismb2018!
# start development server on public ip interface, on port 8000
su -m myuser -c "python manage.py runserver 0.0.0.0:8000 --settings=shared.settings.appglobalconf"
