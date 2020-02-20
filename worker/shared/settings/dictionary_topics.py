from general_types.labels import GOST_LABELS_DICTIONARY, LabelDatastreamGeneric
from utility.utilitydictionaries import UtilityDictionaries
from general_types.enumerations import ObservableGenericType
from typing import Dict, Any, List
import logging

logger = logging.getLogger('textlogger')

PILOT_SELECTED = 'TIVOLI'
GOST_SELECTED = 'GOST_'+PILOT_SELECTED


class GOSTProvider:
    @staticmethod
    def get_datastream(gost: str,
                       id: int) -> str:
        return '{0}/Datastreams({1})/Observations'.format(gost, id)

    @staticmethod
    def get_device_id(pilot_name: str,
                      id: int) -> str:
        return '{0}_{1}'.format(pilot_name,
                                    id)

    @staticmethod
    def get_device_name(pilot_name: str,
                        id: int):
        return 'SFN/Camera/CDL-Estimation/{0}'.format(
            GOSTProvider.get_device_id(pilot_name=pilot_name,
                                       id=id))


def extract_device_id(device_name_complete: str) -> str:
    if not device_name_complete:
        return str()

    if '/' not in device_name_complete:
        return device_name_complete

    list_parts = device_name_complete.split('/')

    return list_parts[-1]


def get_dictionary_observables_topics(things_to_analyze: Dict[str, ObservableGenericType],
                                      local_config_things: Dict[str, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    try:
        if not things_to_analyze or not local_config_things:
            return None

        dict_return = dict()

        for thing_name in things_to_analyze.keys():
            if thing_name not in local_config_things.keys():
                continue

            thing_datastreams = local_config_things[thing_name]

            if not thing_datastreams:
                continue

            if "value" not in thing_datastreams:
                continue

            list_datastreams = thing_datastreams["value"]

            if not list_datastreams:
                continue

            for datastream in list_datastreams:
                if LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID not in datastream.keys():
                    continue

                iot_id = datastream[LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID]
                device_name = UtilityDictionaries.get_dict_field_if(dictionary=datastream,
                                                                    label=LabelDatastreamGeneric.LABEL_DSGENERIC_NAME)
                device_name = extract_device_id(device_name_complete=device_name)

                properties = UtilityDictionaries.get_dict_field_if(dictionary=datastream,
                                                                   label=LabelDatastreamGeneric.LABEL_DSGENERIC_UNITOFMEAS)

                dict_return[iot_id] = {
                    GOST_LABELS_DICTIONARY.LABEL_GOST_DATASTREAMID: GOSTProvider.get_datastream(gost=GOST_SELECTED,
                                                                                                id=iot_id),
                    GOST_LABELS_DICTIONARY.LABEL_GOST_DEVICENAME: device_name,
                    GOST_LABELS_DICTIONARY.LABEL_GOST_UNITOFMEASUREMENTS: properties,
                    GOST_LABELS_DICTIONARY.LABEL_GOST_THING: thing_name
                }
                logger.info('get_dictionary_observables_topics iot_id: {0}, topic: {1}'.format(iot_id,
                                                                                               dict_return[iot_id]))
        return dict_return
    except Exception as ex:
        logger.error('get_dictionary_observables_topics Exception: {}'.format(ex))
        return None
