from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps
import django
from shared.settings.appglobalconf import SCHEDULER_SETTINGS

#from celery.task.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shared.settings.appglobalconf")

app = Celery('jobs', fixups=[])


django.setup()

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


app.conf.beat_schedule = {
    'task_elaboration': {
            'task': 'jobs.tasks.task_provisioning',
            'schedule': SCHEDULER_SETTINGS['TASK_PROVISIONING'],   # Every N seconds
            'options': {'queue': 'taskqueue_provisioning'},
        },
    'task_alive': {
                'task': 'jobs.tasks.task_alive',
                'schedule': SCHEDULER_SETTINGS['TASK_ALIVEAPP'],   # Every N seconds
                'options': {'queue': 'queue_task_alive'},
            },
    # 'task_sw_update_info': {
    #         'task': 'jobs.tasks.task_sw_update_info',
    #         'schedule': 100.0,   #E very N seconds
    #         'options': {'queue': 'queue_sw_update_info'},
    #     },
}