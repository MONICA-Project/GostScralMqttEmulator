from general_types.observables import ObservableGeneric, Localization, CrowdDensityLocalObservation
from general_types.enumerations import ObservableGenericType
from processing.calculate_new_position import CalculatePosition
from utility.utilitydictionaries import UtilityDictionaries
from shared.settings.datastreams import LabelDatastramCamera
from shared.settings.settings import GeoRefArea
from utility.geodesy import GeoPosition
from typing import Dict, Any
import random
import logging
import math

logger = logging.getLogger('textlogger')


class MessageProducer(object):
    ref_pos: GeoPosition = None
    geo_area: GeoRefArea = None
    max_counter_people: int = 2

    @staticmethod
    def set_max_counter_people(max_counter_people: int):
        MessageProducer.set_max_counter_people = max_counter_people

    @staticmethod
    def get_new_observable(
            type_obs: ObservableGenericType,
            device_id: str,
            iot_id: int,
            dictionary_unitofmeasures: Dict[str, Any] = None) -> ObservableGeneric:
        try:
            if type_obs == ObservableGenericType.UNDEFINED:
                logger.info('MessageProducer get_new_observable NO Type Observable Set (None)')
                return None

            if type_obs == ObservableGenericType.LOCALIZATION:
                position = CalculatePosition.calculate_position(ref_pos=MessageProducer.ref_pos,
                                                                georefarea=MessageProducer.geo_area)

                if not position:
                    logger.warning('MessageProducer get_new_observable NO Position Provided')
                    return None

                localization = Localization(tag_id=device_id,
                                            iot_id=iot_id,
                                            lat=position.latitude,
                                            lon=position.longitude)

                logger.info('MessageProducer get_new_observable Position')

                return localization

            elif type_obs == ObservableGenericType.CROWDDENSITYLOCAL:
                density_map_size = UtilityDictionaries.get_dict_field_if(dictionary=dictionary_unitofmeasures,
                                                                         label=LabelDatastramCamera.LABEL_DSCAM_GPS)

                counter_people = random.uniform(a=0,
                                                b=MessageProducer.max_counter_people)
                crowd_density_local = CrowdDensityLocalObservation(device_id=device_id,
                                                                   iot_id=iot_id,
                                                                   map_size=density_map_size)
                crowd_density_local.set_density_map(counter_people=int(math.floor(counter_people)))
                crowd_density_local.consolidate_observable()

                return crowd_density_local

            return None
        except Exception as ex:
            logger.error('MessageProducer get_new_observable Exception: {}'.format(ex))
            return None
