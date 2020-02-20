import signal
import sys
import time
import datetime
import json
import logging

import paho.mqtt.client as mqtt
import arrow

now = arrow.utcnow().format('YYYY-MM-DD_HH-mm')
logging.basicConfig(filename="logs/" + str(now) + ".log", level=logging.DEBUG)
logger = logging.getLogger()


DICTIONARY_OBSERVABLE_TOPICS = {1: ["GOST_TIVOLI/+/Observations"]}
#DICTIONARY_OBSERVABLE_TOPICS = {1: ["#"]}
# from dictionary_catalog_local import DICTIONARY_OBSERVABLE_TOPICS

GOST_URL = "192.168.2.3"
INTERNAL_BROKER_NAME = "mosquitto"
LOCAL = "localhost"

LOCAL_PORT = 1884
BURST_SIZE = 5000


class Settings:
    list_topics = list()
    flag_connection = 0
    flag_subscribe = 0
    counter_message_received = 0
    time_diff = 30
    subscribe_to_all = False
    username = "mosquitto"
    password = "mosquitto"
    mqtt_url = GOST_URL
    mqtt_port = LOCAL_PORT

    @staticmethod
    def initialize_main_list():
        if not DICTIONARY_OBSERVABLE_TOPICS:
            logger.warning("No dictionary!")
            return

        for key in DICTIONARY_OBSERVABLE_TOPICS:
            list_string = DICTIONARY_OBSERVABLE_TOPICS[key]

            if not list_string:
                continue

            # Settings.list_topics.append((list_string[0], 0))
            Settings.list_topics.append((list_string[0], 1))
            # Settings.list_topics.append((list_string[0], 2))


def on_message(client, userdata, message):
    try:
        current_time = arrow.utcnow()

        logger.info("Message topic: " + message.topic)
        logger.info("Message received: " + str(message.payload))
        logger.info("current_time: " + str(current_time.format('YYYY-MM-DD HH:mm:ss')))
        # logger.info("message qos=",message.qos)
        # logger.info("message retain flag=",message.retain)

        string_json = str(message.payload.decode("utf-8"))
        json_received = json.loads(string_json)
        try:
            timestamp_str = json_received["phenomenonTime"]
            timestamp = arrow.get(timestamp_str)
            # timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            diff = current_time - timestamp
            diff_sec = diff.total_seconds()
            logger.info("Message received after: " + str(diff_sec))
            if abs(diff_sec) > Settings.time_diff:
                logger.error(" ---------- Critical ---------- ")
        except KeyError:
            logger.warning("No phenomenonTime.")

        Settings.counter_message_received += 1

        logger.info('OnMessage JSON Conversion Success, counter_messages: {}\n'
                     .format(str(Settings.counter_message_received)))

        if Settings.counter_message_received % BURST_SIZE == 0:
            logger.info("======================================================================\n")

    except Exception as ex:
        logger.critical('Exception OnMessage: {}'.format(ex))


def on_connect(client, userdata, flags, rc):
    try:
        if Settings.flag_connection == 1:
            return

        Settings.flag_connection = 1
        
        if Settings.subscribe_to_all:
            logger.info('Client Connected, subscribe to all topics')
            client.subscribe('#')
            return
        
        counter_topics = len(Settings.list_topics)

        logger.info('Client Connected, Subscribing to {} Elements'.format(str(counter_topics)))
        logger.info(Settings.list_topics)
        client.subscribe(Settings.list_topics)

        # client.subscribe('GOST_IOTWEEK/Datastreams(583)/Observations')
        # client.subscribe('GOST_IOTWEEK/+/Observations')
        # client.subscribe('GOST_LARGE_SCALE_TEST//Antonio/Datastreams')

    except Exception as ex:
        logger.critical('Exception: {}'.format(ex))


def on_disconnect(client: mqtt.Client, userdata, rc):
    try:
        Settings.flag_connection = 0
        logger.debug('Client Disconnected')
        #client.reconnect()
    except Exception as ex:
        logger.critical('Exception: {}'.format(ex))


def on_unsubscribe(client, userdata, level, buf):
    logger.error('Unsubscribed Success! {}'.format(buf))


def on_subscribe(client, userdata, level, buf):
    logger.info('Subscribed Success! {}'.format(len(buf)))


def on_log(client, userdata, level, buf):
    logger.debug('MQTT Log raised: {}'.format(buf))


def convert_stringtime_to_epoch(string_time):
    time.mktime(datetime.datetime.strptime(string_time).timetuple())


def signal_handler(signal, frame):
    """ This signal handler overwrite the default behaviour of SIGKILL (pressing CTRL+C). """

    logger.critical('You pressed Ctrl+C!')
    logger.info("\nThe MQTT listener is turning down now...\n")
    sys.exit(0)


def main(broker_address: str, port: int, username: str = str(), pwd: str = str()):
    print("Creating new instance")
    client = mqtt.Client("LocalClientTest")  # create new instance

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    if username and pwd:
        client.username_pw_set(username=username,password=pwd)

    Settings.initialize_main_list()

    logger.info("Connecting to broker: " + broker_address + ":" + str(port))
    client.connect(host=broker_address, port=port)  # connect to broker
    try:
        print('Prova')
        client.loop_forever()
    except Exception as ex:
        logger.critical('Exception in Main Function: {}'.format(ex))


if __name__ == '__main__':
    
    formatter = "%(asctime)s.%(msecs)04d %(name)-7s %(levelname)s: %(message)s"

#    logging.basicConfig(filename="logs/" + str(now) + ".log", level=logging.DEBUG)
#    logging.getLogger().handlers[0].setFormatter(logging.Formatter(formatter, datefmt="(%b-%d) %H:%M:%S"))
    
    logger.handlers[0].setFormatter(logging.Formatter(formatter, datefmt="(%b-%d) %H:%M:%S"))
    
    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setLevel(logging.INFO)
    std_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(std_handler)

    # signal.signal(signal.SIGINT, signal_handler)

    main(broker_address=Settings.mqtt_url, 
    port=Settings.mqtt_port, 
    username=Settings.username, 
    pwd=Settings.password)
