from jobs.cache_redis import CacheRedisAdapter
from general_types.virtual_classes import ObservableGeneric
# FIXME: Localization to be reviewed
from typing import List, Dict
import logging
import datetime

logger = logging.getLogger('textlogger')


class UtilityCatalogCached:
    LABEL_DICTIONARY_OBS_ALREADYUSED = 'LABEL_DICTIONARY_OBS_BLACKLIST_MAIN'
    LABEL_DICTIONARY_OBSERVABLE_TO_BACKUP = 'DICTIONARY_OBS_TO_BACKUP'
    LABEL_DICTIONARY_OBSERVABLE_NEW = 'DICTIONARY_OBSERVABLE_NEW'
    LABEL_DICTIONARY_TOPICS = 'SERVICEOBSERVATION_DICTIONARY_TOPICS'
    LABEL_DICTIONARY_DEVICE_REGISTRATION = 'DICTIONARY_DEVICEREGISTRATION'

    @staticmethod
    def initialize_catalog() -> bool:
        try:
            CacheRedisAdapter.initialize()

            CacheRedisAdapter.dictionary_create(label_info=UtilityCatalogCached.LABEL_DICTIONARY_TOPICS)
            CacheRedisAdapter.dictionary_create(label_info=UtilityCatalogCached.LABEL_DICTIONARY_DEVICE_REGISTRATION)

            UtilityCatalogCached.configure_catalog_observable_backup(['Localization'])

            return True

        except Exception as ex:
            logger.error('initialize_catalog Exception: {}'.format(ex))
            return False

    @staticmethod
    def configure_catalog_observable_backup(label_list_types: List[str]):
        try:
            CacheRedisAdapter.dictionary_create(label_info=UtilityCatalogCached.LABEL_DICTIONARY_OBSERVABLE_TO_BACKUP)

            for type_observable in label_list_types:
                label_store = UtilityCatalogCached.LABEL_DICTIONARY_OBSERVABLE_TO_BACKUP+type_observable
                CacheRedisAdapter.dictionary_update_value(label_info=UtilityCatalogCached.LABEL_DICTIONARY_OBSERVABLE_TO_BACKUP,
                                                          key=type_observable,
                                                          value=label_store)

        except Exception as ex:
            logger.error('configure_catalog_observable_backup Exception: {}'.format(ex))

    @staticmethod
    def set_catalog_observable_backup(catalog_observable: Dict[str, List[ObservableGeneric]]) -> bool:
        try:
            if not catalog_observable:
                return False

            for type_observable in catalog_observable:
                UtilityCatalogCached.set_list_obstobackup(type_observable=type_observable,
                                                          list_obs_to_backup=catalog_observable[type_observable])

            return True
        except Exception as ex:
            logger.error('set_catalog_observable_backup Exception: {}'.format(ex))
            return False

    @staticmethod
    def set_list_obstobackup(type_observable: str, list_obs_to_backup: List[ObservableGeneric]) -> bool:
        try:
            label_list = UtilityCatalogCached.LABEL_DICTIONARY_OBSERVABLE_TO_BACKUP + type_observable

            return CacheRedisAdapter.set_cache_info(label_info=label_list,
                                                    data=list_obs_to_backup)
        except Exception as ex:
            logger.error('set_list_obstobackup Exception: {}'.format(ex))
            return False

    @staticmethod
    def get_list_obstobackup() -> List[ObservableGeneric]:
        try:
            dictionary_type_observable = \
                CacheRedisAdapter.dictionary_get_all(label_info=UtilityCatalogCached.LABEL_DICTIONARY_OBSERVABLE_TO_BACKUP,
                                                     type_value=str)

            if not dictionary_type_observable:
                return None

            list_return = list()

            for type_observable in dictionary_type_observable:

                if dictionary_type_observable[type_observable] is None:
                    continue

                list_partial = CacheRedisAdapter.get_cached_info(label_info=dictionary_type_observable[type_observable],
                                                                 type_data=list)

                if not list_partial:
                    continue

                list_return.extend(list_partial)
            return list_return

        except Exception as ex:
            logger.error('get_dictionary_specific_observable Exception: {}'.format(ex))
            return None

    @staticmethod
    def confirm_obs_backup() -> bool:
        try:
            dictionary_type_observable = CacheRedisAdapter.\
                dictionary_get_all(label_info=UtilityCatalogCached.LABEL_DICTIONARY_OBSERVABLE_TO_BACKUP,
                                   type_value=str)

            if not dictionary_type_observable:
                return None

            for type_observable in dictionary_type_observable:

                if dictionary_type_observable[type_observable] is None:
                    continue

                CacheRedisAdapter.remove_cache_info(label_info=dictionary_type_observable[type_observable])

            return True
        except Exception as ex:
            logger.error('get_dictionary_specific_observable Exception: {}'.format(ex))
            return False

    @staticmethod
    def get_dictionary_name(label_type_observable: str):
        return '{0}_{1}'.format(UtilityCatalogCached.LABEL_DICTIONARY_OBSERVABLE_NEW,
                                label_type_observable)

    @staticmethod
    def append_new_observable(label_type_observable: str, observable: ObservableGeneric) -> bool:
        try:
            if not observable:
                return False

            return CacheRedisAdapter.dictionary_update_value(label_info=UtilityCatalogCached.get_dictionary_name(label_type_observable),
                                                             key=observable.get_label_cache(),
                                                             value=observable)
        except Exception as ex:
            logger.error('UtilityCatalogCache append_new_observable Exception: {}'.format(ex))
            return False

    @staticmethod
    def get_complete_dictionary_observables(list_type_observables: List[str]) -> Dict[str, ObservableGeneric]:
        try:
            if not list_type_observables:
                logger.warning('UtilityCatalogCache get_complete_dictionary_observables list_type_observable is None')
                return None

            dict_return = dict()

            for type_observable in list_type_observables:
                dict_observable_type = \
                    CacheRedisAdapter.dictionary_get_all(label_info=UtilityCatalogCached.get_dictionary_name(type_observable),
                                                         type_value=ObservableGeneric)
                if not dict_observable_type:
                    logger.info('UtilityCatalogCache get_complete_dictionary_observables not available for type_obs: {}'.format(type_observable))
                    continue

                logger.info('UtilityCatalogCache get_complete_dictionary_observables available for type_obs: {0}, counter_elements: {1}'.format(type_observable,
                                                                                                                                                len(dict_observable_type)))

                dict_return[type_observable] = dict_observable_type

            return dict_return
        except Exception as ex:
            logger.error('UtilityCatalogCache: get_complete_dictionary_observables Exception: {}'.format(ex))
            return None

    @staticmethod
    def get_last_observable(label_observable: str) -> ObservableGeneric:
        try:
            return CacheRedisAdapter.get_cached_info(label_info=label_observable,
                                                     type_data=ObservableGeneric)
        except Exception as ex:
            logger.error('get_mostrecent_observable Exception: {}'.format(ex))
            return None

    @staticmethod
    def check_observable_new(dictionary_obs_time: Dict[str, datetime.datetime], observable: ObservableGeneric) -> bool:
        try:
            if not observable:
                return False

            if not dictionary_obs_time:
                return True

            if observable.get_label_cache() not in dictionary_obs_time \
                    or not dictionary_obs_time[observable.get_label_cache()]:
                return True

            timestamp_prev_obs = dictionary_obs_time[observable.get_label_cache()]
            timestamp_curr_obs = observable.get_timestamp()

            if (timestamp_curr_obs - timestamp_prev_obs).total_seconds() <= 0:
                return False

            return True
        except Exception as ex:
            logger.error('check_observable_new {}'.format(ex))
            return True

    @staticmethod
    def get_observationlist_specifictype(type_observable: str,
                                         list_mqtttopics_admitted: List[str],
                                         dictionary_singletype_observables: Dict[str, ObservableGeneric],
                                         dictionary_obs_time: Dict[str, datetime.datetime]) -> List[ObservableGeneric]:

        list_observable_singletype = list()

        for mqtt_topic in dictionary_singletype_observables:
            single_observation = dictionary_singletype_observables[mqtt_topic]

            if not single_observation:
                logger.info('UtilityCatalogCache get_observationlist_specifictype not observable')
                continue

            if not UtilityCatalogCached.check_observable_new(dictionary_obs_time=dictionary_obs_time,
                                                             observable=single_observation):
                continue

            list_observable_singletype.append(single_observation)

        return list_observable_singletype

    @staticmethod
    def append_topic(single_topic: str) -> bool:
        try:
            CacheRedisAdapter.dictionary_update_value(label_info=UtilityCatalogCached.LABEL_DICTIONARY_TOPICS,
                                                      key=single_topic,
                                                      value=1)
        except Exception as ex:
            logger.info('UtilityCatalogCached store_catalog_datastreams Exception: {}'.format(ex))
            return False

    @staticmethod
    def get_list_topics() -> List[str]:
        try:
            dictionary_topics = CacheRedisAdapter.\
                dictionary_get_all(label_info=UtilityCatalogCached.LABEL_DICTIONARY_TOPICS,
                                   type_value=str)

            list_topics = list()
            for key in dictionary_topics:
                if not key:
                    continue
                list_topics.append(key)

            return list_topics
        except Exception as ex:
            logger.info('UtilityCatalogCached store_catalog_datastreams Exception: {}'.format(ex))
            return False

