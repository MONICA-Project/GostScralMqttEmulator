from pymongo import MongoClient
from shared.settings.appglobalconf import MONGO_DB_CONFIGURATION
import logging
from typing import Iterable

logger = logging.getLogger(name='textlogger')


class UtilityMongoDB:
    mongo_db_client = None
    handle_database = None
    handle_collection = None
    host_address = str()

    @staticmethod
    def set_host_address():
        UtilityMongoDB.host_address = '{0}:{1}'.format(MONGO_DB_CONFIGURATION['MONGODB_HOSTNAME'],
                                                       MONGO_DB_CONFIGURATION['MONGODB_TCP_PORT'])

    @staticmethod
    def initialize():
        try:
            UtilityMongoDB.set_host_address()

            UtilityMongoDB.mongo_db_client = MongoClient(host=UtilityMongoDB.host_address,
                                                         username=MONGO_DB_CONFIGURATION['MONGODB_USERNAME'],
                                                         password=MONGO_DB_CONFIGURATION['MONGODB_PASSWORD'])

            UtilityMongoDB.handle_database = UtilityMongoDB.mongo_db_client[
                MONGO_DB_CONFIGURATION['MONGODB_DATABASE_NAME']
            ]

            UtilityMongoDB.handle_collection = UtilityMongoDB.handle_database[MONGO_DB_CONFIGURATION['MONGODB_DATABASE_COLLECTION']]

            # dictionary_element = {"TESTSW": 2}
            #
            # result = collection_new.insert_one(dictionary_element)

        except Exception as ex:
            logger.error('UtilityMongoDB initialize Exception: {}'.format(ex))

    @staticmethod
    def close() -> bool:
        try:
            if not UtilityMongoDB.mongo_db_client:
                return False

            UtilityMongoDB.mongo_db_client.close()
            UtilityMongoDB.mongo_db_client = None
        except Exception as ex:
            logger.error('UtilityMongoDB Close Exception: {}'.format(ex))

    @staticmethod
    def get_collections_global_count() -> int:
        try:
            if not UtilityMongoDB.mongo_db_client:
                return -1

            return UtilityMongoDB.handle_collection.count()
        except Exception as ex:
            logger.error('UtilityMongoDB global_count Exception: {}'.format(ex))
            return 0

    @staticmethod
    def save_observable(json_message: dict):
        try:
            UtilityMongoDB.handle_collection.insert_one(json_message)
            logger.debug('UtilityMongoDB save info done')
        except Exception as ex:
            logger.error('UtilityMongoDB initialize Exception: {}'.format(ex))

    @staticmethod
    def save_many_observable(collection_json_messages: Iterable):
        try:
            UtilityMongoDB.handle_collection.insert_many(documents=collection_json_messages)
            logger.debug('UtilityMongoDB save info done')
        except Exception as ex:
            logger.error('UtilityMongoDB initialize Exception: {}'.format(ex))
