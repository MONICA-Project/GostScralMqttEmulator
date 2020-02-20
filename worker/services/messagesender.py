from services.mqtt_publisher import ServerMQTT
from services.messageproducer import MessageProducer
from shared.settings.settings import GeoRefArea
from general_types.labels import GOST_LABELS_DICTIONARY
from general_types.enumerations import ObservableGenericType
from utility.geodesy import GeoPosition
from utility.utilitydictionaries import UtilityDictionaries
from typing import List, Dict, Any

import logging

logger = logging.getLogger('textlogger')


class Publisher(object):
    @staticmethod
    def set_topics(topics: List[str]):
        ServerMQTT.set_topics(topics=topics)

    @staticmethod
    def configure(client_id: str,
                  hostname: str,
                  port: int,
                  username: str = str(),
                  pwd: str = str()):
        logger.info('Try Connecting MQTT Client on {0} Port: {1}, User: {2}, PWD: {3}'.format(hostname,
                                                                                              port,
                                                                                              username,
                                                                                              pwd))
        ServerMQTT.configure_client(client_id=client_id,
                                    hostname=hostname,
                                    port=port,
                                    username=username,
                                    pwd=pwd)

    @staticmethod
    def connect():
        ServerMQTT.connect_client()

    @staticmethod
    def loop_wait():
        ServerMQTT.loop_wait()

    @staticmethod
    def loop_start():
        ServerMQTT.loop_start()

    @staticmethod
    def stop_client():
        ServerMQTT.stop_client()

    @staticmethod
    def set_reference_geo_area(geo_area: GeoRefArea) -> bool:
        try:
            if not geo_area:
                return False
            MessageProducer.geo_area = geo_area
            MessageProducer.ref_pos = GeoPosition(latitude=geo_area.reference_pos_lat,
                                                  longitude=geo_area.reference_pos_long,
                                                  altitude=0,
                                                  request_ecef_conf=True)
            return True
        except Exception as ex:
            logger.error('set_reference_geo_area Exception: {}'.format(ex))
            return False

    @staticmethod
    def extract_device_id(topic: str) -> str:
        if not topic:
            return str()

        if '/' not in topic:
            return topic

        list_parts = topic.split('/')

        return list_parts[-1]

    @staticmethod
    def publish_topics(dictionary_observables: Dict[int, Dict[str, str]],
                       translate_map: Dict[str, ObservableGenericType]) -> bool:
        try:
            if not dictionary_observables:
                logger.info('publish_topics NO Dictionary to Publish')
                return False

            counter_message_sent = 0

            for iot_id in dictionary_observables:
                dict_topic_deviceid = dictionary_observables[iot_id]

                if GOST_LABELS_DICTIONARY.LABEL_GOST_DATASTREAMID not in dict_topic_deviceid.keys():
                    continue

                if GOST_LABELS_DICTIONARY.LABEL_GOST_DEVICENAME not in dict_topic_deviceid.keys():
                    continue

                if GOST_LABELS_DICTIONARY.LABEL_GOST_THING not in dict_topic_deviceid.keys():
                    continue

                topic = dict_topic_deviceid[GOST_LABELS_DICTIONARY.LABEL_GOST_DATASTREAMID]
                device_id = dict_topic_deviceid[GOST_LABELS_DICTIONARY.LABEL_GOST_DEVICENAME]
                properties = UtilityDictionaries.get_dict_field_if(dictionary=dict_topic_deviceid,
                                                                   label=GOST_LABELS_DICTIONARY.LABEL_GOST_UNITOFMEASUREMENTS)

                thing_name = UtilityDictionaries.get_dict_field_if(dictionary=dict_topic_deviceid,
                                                                   label=GOST_LABELS_DICTIONARY.LABEL_GOST_THING)

                observable_type = UtilityDictionaries.get_dict_field_if(dictionary=translate_map,
                                                                        label=thing_name,
                                                                        none_value=ObservableGenericType.UNDEFINED)

                logger.info('MQTT Publisher Topic: {0}, DeviceID: {1}'.format(topic,
                                                                              device_id))

                observable = MessageProducer.get_new_observable(
                    type_obs=observable_type,
                    device_id=device_id,
                    iot_id=iot_id,
                    dictionary_unitofmeasures=properties
                )

                if not observable:
                    continue

                ServerMQTT.publish(topic=topic,
                                   dictionary=observable.to_dictionary())

                counter_message_sent += 1

                if (counter_message_sent % 10) == 0:
                    logger.info('MQTT Publish Messages: {}'.format(counter_message_sent))

            logger.info('MQTT Publish Messages Completed: {}'.format(counter_message_sent))
        except Exception as ex:
            logger.error('Exception publish_topics: {}'.format(ex))
