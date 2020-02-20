import logging
from jobs.cache_redis import CacheRedisAdapter
from utility.utility_database import UtilityDatabase
from utility.utility_catalog_cached import UtilityCatalogCached
from shared.settings.appglobalconf import LOCAL_CONFIG, LocConfLbls

logger = logging.getLogger('textlogger')


class UtilityStartupApplication:
    @staticmethod
    def startup():
        UtilityCatalogCached.initialize_catalog()

    @staticmethod
    def trace_startup_info():
        try:
            logger.info("HLDFAD MODULE STARTED, VERSION: {0}".format(LOCAL_CONFIG[LocConfLbls.LABEL_SW_RELEASE_VERSION]))

            for key in LOCAL_CONFIG:
                if "SW_RELEASE_VERSION" == key:
                    continue

                logger.info(" - {0}: {1}"
                            .format(key, LOCAL_CONFIG[key]))

        except Exception as ex:
            logger.error('UtilityStartupApplication trace_startup_info Exception: {}'.format(ex))

    @staticmethod
    def adjust_startup_data():
        try:

            UtilityDatabase.purge_db_connections()
            UtilityDatabase.update_database_startup()

            # CacheRedisAdapter.test_example()

            # crowd_heatmap_outputs = UtilityDatabase.get_list_crowdheatmap_not_transferred(LOCAL_CONFIG[LocConfLbls.LABEL_PILOT_NAME])
            # crowd_heatmap_ids = UtilityDatabase.extract_crowd_heatmap_ids(crowd_heatmap_outputs)
            running_id = UtilityDatabase.update_get_sw_running_info(LOCAL_CONFIG[LocConfLbls.LABEL_SW_RELEASE_VERSION])

            logger.info('UtilityStartupApplication Running ID: {0} SW_VERSION: {1}'
                        .format(str(running_id),
                                LOCAL_CONFIG[LocConfLbls.LABEL_SW_RELEASE_VERSION]))
        except Exception as ex:
            logger.error('UtilityStartupApplication adjust_startup_data Exception: {}'.format(ex))