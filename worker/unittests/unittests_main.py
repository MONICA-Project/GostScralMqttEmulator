import logging
from typing import List, Dict

logger = logging.getLogger('textlogger')


class UnitTestMain:
    @staticmethod
    def print_report(dictionary_test_results: Dict[str, bool] = dict()):
        if not dictionary_test_results:
            return

        for key in dictionary_test_results:
            logger.info('UnitTestName: {0}, Result: {1}'.format(key, dictionary_test_results[key]))

    @staticmethod
    def launch_all_tests(enable_tests: bool = False, list_enabled_tests: List[str] = list()) \
            -> Dict[str, bool]:
        try:
            if not enable_tests or not list_enabled_tests:
                return None

            dict_results = dict()

            for test_name in list_enabled_tests:
                print('Launching Test: {}'.format(test_name))

            return dict_results
        except Exception as ex:
            logger.error('UnitTestMain Execution Exception: {}'.format(ex))
            return None
