from utility.utility_database import UtilityDatabase
from jobs.cache_redis import CachedComponents
from shared.settings.appglobalconf import LOCAL_CONFIG, LocConfLbls
import datetime
import pytz
import logging

logger = logging.getLogger('textlogger')


class UtilitySWUpdateInfo:
    @staticmethod
    def update_sw_info_realtime():
        try:
            UtilityDatabase.purge_db_connections()

            sw_version = LOCAL_CONFIG[LocConfLbls.LABEL_SW_RELEASE_VERSION]
            counter_observables = CachedComponents.get_last_observable_id()
            counter_output = CachedComponents.get_counter_crowd_heatmap_output()
            counter_wristband_registered = CachedComponents.get_counter_datastreams_registered(datastream_feature='Localization')
            current_timestamp = datetime.datetime.now(tz=pytz.utc)

            UtilityDatabase.update_sw_running_timestop(sw_version=sw_version,
                                                       timestamp_stop=current_timestamp,
                                                       counter_message_output=counter_output,
                                                       counter_observables=counter_observables,
                                                       counter_device_registered=counter_wristband_registered)

            logger.info('UtilitySWUpdateInfo Updated Info now, '
                        'counterObs: {0}, CounterOutput: {1}, '
                        'CounterDevRegister: {2}'
                        .format(str(counter_observables),
                                str(counter_output),
                                str(counter_wristband_registered))
                        )
        except Exception as ex:
            logger.error('UtilitySWUpdateInfo Exception: {}'.format(ex))



