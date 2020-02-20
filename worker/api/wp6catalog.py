from typing import Dict, Any, List
from utility.utilitydictionaries import UtilityDictionaries
from os import environ
import logging

logger = logging.getLogger('textlogger')


class WP6Catalog:
    LABEL_CATALOG_DATASTREAMID = "dataStreamId"
    LABEL_CATALOG_MQTTTOPIC = "mqttTopic"
    LABEL_CATALOG_MQTTSERVER = "mqttServer"
    LABEL_CATALOG_EXTERNALID = "externalId"
    LABEL_CATALOG_METADATA = "metadata"
    LABEL_CATALOG_SENSORTYPE = "sensorType"
    LABEL_CATALOG_UNITOFMEASUREMENT = "unitOfMeasurement"
    LABEL_CATALOG_FIXEDLATITUDE = "fixedLatitude"
    LABEL_CATALOG_FIXEDLONGITUDE = "fixedLongitude"

    DATASTREAM_ID_QUEUEDETECTIONALERT = 13150
    DATASTREAM_ID_CROWDHEATMAPOUTPUT = 13151
    DATASTREAM_ID_UNKNOWN = 13148

    WRONG_ANSWER = {"WrongAnswer": "None"}

    CONVERSION_DATASTREAM = {
        "HLDFAD:QueueDetectionAlert": DATASTREAM_ID_QUEUEDETECTIONALERT,
        "HLDFAD:PeopleHetmap": DATASTREAM_ID_CROWDHEATMAPOUTPUT
                             }

    @staticmethod
    def get_datastream_id(external_id: str) -> int:
        return UtilityDictionaries.get_dict_field_if(dictionary=WP6Catalog.CONVERSION_DATASTREAM,
                                                     label=external_id,
                                                     none_value=WP6Catalog.DATASTREAM_ID_UNKNOWN)

    @staticmethod
    def get_list_fixed_fields() -> List[str]:
        return [
            WP6Catalog.LABEL_CATALOG_EXTERNALID,
            WP6Catalog.LABEL_CATALOG_SENSORTYPE,
            WP6Catalog.LABEL_CATALOG_UNITOFMEASUREMENT,
            WP6Catalog.LABEL_CATALOG_METADATA,
            WP6Catalog.LABEL_CATALOG_FIXEDLATITUDE,
            WP6Catalog.LABEL_CATALOG_FIXEDLONGITUDE
        ]

    @staticmethod
    def create_thing(dict_input: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not dict_input:
                return WP6Catalog.WRONG_ANSWER

            dict_output: Dict[str, Any] = dict()

            logger.info('create_thing create Dictionary')

            list_fixed_fields = WP6Catalog.get_list_fixed_fields()

            if not list_fixed_fields:
                return WP6Catalog.WRONG_ANSWER

            for field in list_fixed_fields:
                dict_output[field] = UtilityDictionaries.get_dict_field_if(dictionary=dict_input,
                                                                           label=field)

            exposed_mqtt_host = environ.get('EXPOSED_MQTT_HOST', '127.0.0.1')
            exposed_mqtt_port = environ.get('EXPOSED_MQTT_PORT', '1884')

            logger.info('create_thing mqtt={0}:{1}'.format(exposed_mqtt_host,
                                                           exposed_mqtt_port))
            external_id = UtilityDictionaries.get_dict_field_if(dictionary=dict_input,
                                                                label=WP6Catalog.LABEL_CATALOG_EXTERNALID,
                                                                none_value="unknown")
            dict_output[WP6Catalog.LABEL_CATALOG_DATASTREAMID] = WP6Catalog.get_datastream_id(external_id=external_id)
            dict_output[WP6Catalog.LABEL_CATALOG_MQTTTOPIC] = "GOST_TIVOLI/Datastreams({})/Observations".format(external_id)
            dict_output[WP6Catalog.LABEL_CATALOG_MQTTSERVER] = "{0}:{1}".format(exposed_mqtt_host,
                                                                                exposed_mqtt_port)

            logger.info('DICT Output={}'.format(dict_output))

            return dict_output
        except Exception as ex:
            logger.error('WP6Catalog create_thing Exception: {}'.format(ex))
            return WP6Catalog.WRONG_ANSWER







