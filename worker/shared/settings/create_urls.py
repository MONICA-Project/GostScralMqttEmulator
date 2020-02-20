from shared.settings.appglobalconf import GOST_DB_THINGS
from shared.settings.settings import Settings
from general_types.labels import LabelThingsName, LabelDatastreamGeneric
from django.urls import path
from typing import List, Optional, Any
from api.views import GostDBSFNDatastreams, \
    GostDBWristbandDatastreams, GostDBThings

import logging

logger = logging.getLogger('textlogger')


def create_single_path(iot_id: int,
                       thing_name: str) -> path:
    try:
        url_string = 'v1.0/Things({0})/Datastreams'.format(iot_id)

        if thing_name == LabelThingsName.LABEL_THING_SFN:
            logger.info('Creating SFN Path: {}'.format(url_string))
            return path(url_string, GostDBSFNDatastreams.as_view())
        elif thing_name == LabelThingsName.LABEL_THING_WRISTBAND:
            logger.info('Creating WB-GW Path: {}'.format(url_string))
            return path(url_string, GostDBWristbandDatastreams.as_view())

        logger.info('NO PATH Created: {}'.format(url_string))

        return None
    except Exception as ex:
        logger.error('create_single_path Exception: {}'.format(ex))
        return None


def create_paths_datastreams() -> List[path]:
    try:
        path_thing = path('v1.0/Things', GostDBThings.as_view())

        if not Settings.THINGS_TO_ANALYSE or not GOST_DB_THINGS:
            return [path_thing]

        if "value" not in GOST_DB_THINGS:
            return [path_thing]

        LIST_THINGS = GOST_DB_THINGS["value"]

        if not LIST_THINGS:
            logger.info('create_paths_datastreams Empty List_Things')
            return None

        list_paths: List[path] = list()
        list_paths.append(path_thing)

        for thing_name in Settings.THINGS_TO_ANALYSE:
            for thing in LIST_THINGS:
                if not thing or LabelDatastreamGeneric.LABEL_DSGENERIC_NAME not in thing \
                        or LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID not in thing:
                    logger.warning('create_paths_datastreams No parameters found on thing: {}'.format(thing))
                    continue

                iot_id = thing[LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID]

                if thing[LabelDatastreamGeneric.LABEL_DSGENERIC_NAME] == thing_name:
                    path_to_add = create_single_path(iot_id=iot_id,
                                                     thing_name=thing_name)

                    if not path_to_add:
                        logger.warning('create_paths_datastreams PATH_TO_ADD IS None')
                        continue

                    list_paths.append(path_to_add)
                else:
                    logger.info('create_paths_datastreams NO Matching: {0} vs {1}'.format(thing["name"], thing_name))

        if not list_paths:
            logger.info('create_paths_datastreams NO Path to add')
            return None

        logger.info('create_paths_datastreams {} path to append'.format(len(list_paths)))

        return list_paths
    except Exception as ex:
        logger.error('create_paths_datastreams Exception: {}'.format(ex))
        return None
