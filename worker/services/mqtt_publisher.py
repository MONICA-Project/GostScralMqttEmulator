import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish  # FIXME: REMOVE (It is just for test)
import json
from typing import Dict, Any, List
import datetime
import logging
from jobs.cache_redis import CacheRedisAdapter

logger = logging.getLogger('textlogger')


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat() + 'Z'

        return json.JSONEncoder.default(self, o)


class SettingsMQTT(object):
    def __init__(self,
                 hostname: str = str(),
                 port: int = 0,
                 client_id: str = str(),
                 username: str = str(),
                 password: str = str()):
        self.hostname = hostname
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.dict_auth = dict()
        self.set_dict_auth(username=username,
                           pwd=password)

    def set_dict_auth(self,
                      username: str,
                      pwd: str) -> bool:
        if not username or not pwd:
            return False

        self.dict_auth['username'] = username
        self.dict_auth['password'] = pwd

    def get_auth_dictionary(self) -> Dict[str, str]:
        if not self.dict_auth:
            return None

        return self.dict_auth


class ServerMQTT(object):
    LABEL_TOPICS = 'SERVERMQTT_TOPICS'
    client_mqtt = None
    flag_connected = 0
    counter_message_published = 0
    debug_numbernotification = 1
    settings_mqtt = SettingsMQTT()
    port = 0
    reference_datetime = None

    @staticmethod
    def get_client_mqtt() -> mqtt.Client:
        return ServerMQTT.client_mqtt

    @staticmethod
    def subscribe_topic_lists(topics: List[str]) -> bool:
        try:
            if not topics:
                return False

            if not ServerMQTT.client_mqtt:
                return False

            list_tuple = list()

            for topic in topics:
                if not topic:
                    continue
                list_tuple.append((topic, 0))

            ServerMQTT.get_client_mqtt().subscribe(topic=list_tuple)
            logger.info('ServerMQTT Subscription to topics')
        except Exception as ex:
            logger.error('subscribe_topic_lists Exception: {}'.format(ex))
            return False

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        try:
            if ServerMQTT.flag_connected == 1:
                return

            topics = CacheRedisAdapter.get_cached_info(label_info=ServerMQTT.LABEL_TOPICS,
                                                       type_data=list)

            ServerMQTT.subscribe_topic_lists(topics=topics)

            ServerMQTT.flag_connected = 1

            logger.info('ServerMQTT on_connect event')
        except Exception as ex:
            logger.error('Exception: {}'.format(ex))

    @staticmethod
    def on_log(client, userdata, level, buf):
        logger.info('ServerMQTT Log raised: {}'.format(buf))

    @staticmethod
    def on_disconnect(client: mqtt.Client, userdata, rc):
        try:
            ServerMQTT.flag_connected = 0

            logger.info('ServerMQTT Disconnected')
        except Exception as ex:
            logger.error('ServerMQTT on_disconnect Exception: {}'.format(ex))

    @staticmethod
    def on_subscribe(client: mqtt.Client, userdata, mid, granted_qos):
        try:
            logger.error('ServerMQTT on_subscribe Raised')
        except Exception as ex:
            logger.error('ServerMQTT on_subscribe Exception: {}'.format(ex))

    @staticmethod
    def on_publish(client, userdata, result):
        try:
            logger.info('ServerMQTT OnPublish Raised')
            ServerMQTT.counter_message_published += 1

            if (ServerMQTT.counter_message_published % ServerMQTT.debug_numbernotification) == 0:
                interval_secs = (datetime.datetime.utcnow()-ServerMQTT.reference_datetime).total_seconds()
                logger.info('ServerMQTT OnPublish Method raised: {0} RelativeTime: {1}'.format(ServerMQTT.counter_message_published,
                                                                                         interval_secs))
        except Exception as ex:
            logger.error('ServerMQTT OnPublish Exception: {}'.format(ex))

    @staticmethod
    def configure_client(client_id: str,
                         hostname: str,
                         port: int,
                         username: str = str(),
                         pwd: str = str()) -> bool:
        try:
            ServerMQTT.client_mqtt = mqtt.Client(client_id=client_id, clean_session=True)
            ServerMQTT.client_mqtt.on_connect = ServerMQTT.on_connect
            ServerMQTT.client_mqtt.on_disconnect = ServerMQTT.on_disconnect
            ServerMQTT.client_mqtt.on_subscribe = ServerMQTT.on_subscribe
            ServerMQTT.client_mqtt.on_publish = ServerMQTT.on_publish
            ServerMQTT.client_mqtt.on_log = ServerMQTT.on_log
            ServerMQTT.hostname = hostname
            ServerMQTT.port = port

            ServerMQTT.settings_mqtt = SettingsMQTT(hostname=hostname,
                                                    port=port,
                                                    username=username,
                                                    password=pwd)

            if not username or not pwd:
                logger.info('ServerMQTT configure_client NO Credential Set')
                return True

            logger.info('ServerMQTT configure_client set Username and PWD: {}'.format(username))

            ServerMQTT.client_mqtt.username_pw_set(username=username,
                                                   password=pwd)
            return True
        except Exception as ex:
            logger.error('ServerMQTT configure_client Exception: {}'.format(ex))

    @staticmethod
    def set_topics(topics: List[str]) -> bool:
        try:
            if not topics:
                return False

            CacheRedisAdapter.set_cache_info(label_info=ServerMQTT.LABEL_TOPICS,
                                             data=topics)
            return True
        except Exception as ex:
            logger.error('ServerMQTT set_topics Exception: {}'.format(ex))
            return False

    @staticmethod
    def stop_client():
        try:
            ServerMQTT.get_client_mqtt().disconnect()
            ServerMQTT.get_client_mqtt().loop_stop()
        except Exception as ex:
            logger.error('ServerMQTT stop_client Exception: {}'.format(ex))

    @staticmethod
    def connect_client():
        try:
            # logger.info(
            #     'ServerMQTT configure_client trying connect hostname: {0}, port: {1}'.format(ServerMQTT.hostname, ServerMQTT.port))
            # ServerMQTT.client_mqtt.connect(host=ServerMQTT.hostname,
            #                                port=ServerMQTT.port)
            logger.info('ServerMQTT configure_client hostname: {0}, port: {1}'.format(ServerMQTT.hostname, ServerMQTT.port))
            ServerMQTT.reference_datetime = datetime.datetime.utcnow()
        except Exception as ex:
            logger.error('ServerMQTT connect_client Exception: {}'.format(ex))

    @staticmethod
    def loop_start():
        try:
            logger.info('ServerMQTT Loop Start')
            # ServerMQTT.get_client_mqtt().loop_start()
        except Exception as ex:
            logger.error('ServerMQTT Loop Forever Exception: {}'.format(ex))

    @staticmethod
    def loop_wait():
        try:
            logger.info('ServerMQTT Loop Forever')
            ServerMQTT.get_client_mqtt().loop_forever()
        except Exception as ex:
            logger.error('ServerMQTT Loop Forever Exception: {}'.format(ex))

    @staticmethod
    def publish(topic: str,
                dictionary: Dict[str, Any]) -> bool:
        try:
            if not ServerMQTT.client_mqtt:
                logger.warning('ServerMQTT Publish NOT DONE')
                return False

            if not dictionary:
                logger.warning('No Datat To Transfer')
                return False

            # print('Try Sending MQTT Message publish_bis....')

            string_json = json.dumps(obj=dictionary,
                                     cls=DateTimeEncoder)

            publish.single(topic=topic,
                           payload=string_json,
                           hostname=ServerMQTT.settings_mqtt.hostname,
                           port=ServerMQTT.settings_mqtt.port,
                           retain=False,
                           auth=ServerMQTT.settings_mqtt.get_auth_dictionary(),
                           client_id=ServerMQTT.settings_mqtt.client_id
                           )

            # return_info = ServerMQTT.client_mqtt.publish(topic=topic,
            #                                              payload=string_json,
            #                                              qos=0,
            #                                              retain=False)
            #
            # if not return_info:
            #     logger.warning('ServerMQTT Publish Failed return_info is None')
            #     return False
            #
            # if return_info.rc != mqtt.MQTT_ERR_SUCCESS:
            #     logger.warning('ServerMQTT Publish Error: {}'.format(str(return_info.rc)))
            #     return False
            #
            # return_info.wait_for_publish()

            logger.info('ServerMQTT Publish Success, topic: {}'.format(topic))

            # print('Success Sending publish_bis: {}'.format(string_json))
            return True
        except Exception as ex:
            logger.error('Exception ServerMQTT PublishBis: {}'.format(ex))
            return False
