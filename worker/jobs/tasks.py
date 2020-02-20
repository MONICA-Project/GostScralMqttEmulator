#!/usr/bin/env python

from shared.celery_settings import app
from shared.settings.appglobalconf import LOCAL_CONFIG_THINGS
from celery.signals import celeryd_after_setup
from services.messagesender import Publisher, MessageProducer
from shared.settings.settings import Settings
from shared.settings.dockersconf import CACHE_REDIS_CONFIGURATION
import datetime
from shared.settings.dictionary_topics import get_dictionary_observables_topics
from jobs.cache_redis import CacheRedisAdapter

import celery

import logging

logger = logging.getLogger('textlogger')


class WorkerTasks(celery.Task):
    alive_counter = 0

    def run(self, *args, **kwargs):
        logging.info('WorkerTasks RUNNING METHOD CALLED')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.info('{0!r} failed: {1!r}'.format(task_id, exc))

    def after_return(self, *args, **kwargs):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logging.info('WorkerTasks ON RETRY METHOD')

    def on_success(self, retval, task_id, args, kwargs):
        logging.info('WorkerTasks SUCCESS ACTIVATION WORKERTASK')

    def shadow_name(self, args, kwargs, options):
        logging.info('WorkerTasks SHADOW NAME')

    @staticmethod
    def periodic_publish() -> bool:
        try:
            if Settings.list_events_publish:
                return
            Settings.list_events_publish.append(1)
            logger.info('Called periodic publish, time: {}'.format(datetime.datetime.utcnow().isoformat()))

            dictionary_topics = get_dictionary_observables_topics(things_to_analyze=Settings.THINGS_TO_ANALYSE,
                                                                  local_config_things=LOCAL_CONFIG_THINGS)

            Publisher.publish_topics(dictionary_observables=dictionary_topics,
                                     translate_map=Settings.THINGS_TO_ANALYSE)
            Settings.list_events_publish.clear()
            return True
        except Exception as ex:
            logging.error('periodic_publish Exception: {}'.format(ex))
            return False

    @staticmethod
    def request_launch_task_provisioning():
        try:
            logger.info('WorkerTask request_launch_task_provisioning')
        except Exception as ex:
            logger.error('request_launch_task_provisioning Exception: {}'.format(ex))

    @staticmethod
    def request_launch_task_sw_update():
        try:
            logger.info('WorkerTask request_launch_task_sw_update')
            task_sw_update_info.apply_async(args=["{'Prova':1}"],
                                            queue='queue_sw_update_info',
                                            serializer='json')
        except Exception as ex:
            logger.error('request_launch_task_sw_update Exception: {}'.format(ex))


@app.task(bind=True, typing=False, serializer='json', base=WorkerTasks)
def first(self, data):
    try:
        return {"status": True}
    except Exception as ex:
        logger.error('First Task Exception: {}'.format(ex))


@app.task(bind=True, typing=False, serializer='json', base=WorkerTasks)
def check_db(self):
    # TODO
    return {"status": True}


@app.task(bind=True, typing=False, serializer='json', base=WorkerTasks)
def task_sw_update_info(self, data):
    try:
        return {"status": True}
    except Exception as ex:
        logger.error('Task Discover Devices Exception: {}'.format(ex))
        return {"status": False}


@app.task(bind=True, typing=False, serializer='json', base=WorkerTasks)
def task_alive(self):
    try:
        logger.info('TASK ALIVE CALLED Counter: {}'.format(WorkerTasks.alive_counter))
        WorkerTasks.alive_counter += 1

        return {"status": True}
    except Exception as ex:
        logger.error('TASK ALIVE EXCEPTION: {}'.format(ex))
        return {"status": False}


@app.task(bind=True, typing=False, serializer='json', base=WorkerTasks)
def task_provisioning(self):
    try:
        logger.info('TASK PROVISIONING ACTIVE')
        WorkerTasks.periodic_publish()
        return {"status": True}

    except Exception as ex:
        logger.error('task_elaboration Exception: {}'.format(ex))
        return {"status": False}


@celeryd_after_setup.connect()
def broker_connection(sender, instance, **kwargs):
    try:
        logger.info('broker_connection Application Initialization Launched')

        CacheRedisAdapter.initialize(cache_redis_configuration=CACHE_REDIS_CONFIGURATION)

        Settings.retrieve_environment_settings()
        Publisher.configure(client_id=Settings.client_id,
                            hostname=Settings.hostname,
                            port=Settings.port,
                            username=Settings.username,
                            pwd=Settings.password)
        dict_obs_topics = get_dictionary_observables_topics(things_to_analyze=Settings.THINGS_TO_ANALYSE,
                                                            local_config_things=LOCAL_CONFIG_THINGS)
        topics = Settings.get_list_topics(dictionary_obs_topics=dict_obs_topics)
        Publisher.set_topics(topics=topics)

        MessageProducer.set_max_counter_people(Settings.max_counter_people_densitymap)
        Publisher.set_reference_geo_area(geo_area=Settings.geographic_area)
        Publisher.loop_start()
        Publisher.connect()
        logger.info('broker_connection Application Initialization Done')

        return {"status", True}
    except Exception as ex:
        logger.error('broker_connection Launched Exception: {}'.format(ex))
        return {"status", False}
