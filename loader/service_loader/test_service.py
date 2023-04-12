import datetime
import pytz
from typing import List, Dict

from loader.service_loader import TestInfo
from loader.service_loader.basic_rest_service import BasicRestService


class TestService:
    TIMEZONE = pytz.timezone("UTC")

    def get_recent_results(self, from_: datetime.datetime) -> List[TestInfo]:
        """Return list of TestInfo instances received from REST API service."""
        raise NotImplementedError(f"{self.__class__}.get_recent_results is not implemented")

    def get_result_by_id(self, test_id: int) -> Dict:
        """Return calculated test results received from REST API service."""
        raise NotImplementedError(f"{self.__class__}.get_results_by_id is not implemented")


class DefaultTestService(TestService, BasicRestService):
    """DefaultTestService contatins simple straightforward implementation of two requests common
    for the following services:
    1. Burnout
    2. Distress - FIXME: distress service has API different from other services, and it would be fixed later.
    3. Coping
    4. SPB
    """

    def __init__(self, host: str, port: int, token: str):
        BasicRestService.__init__(self, host, port, token)
        self._test_info_path = 'api/v1/results/recent'
        self._test_result_path = 'api/v1/results'


    def get_recent_results(self, from_: datetime.datetime) -> List[TestInfo]:
        from_timestamp = int(from_.astimezone(TestService.TIMEZONE).timestamp())
        try:
            response = self.make_request(f"{self._test_info_path}", params={'from': from_timestamp})
        except Exception as e:
            self._logger.error("Failed to request recent results")
            return []

        if not isinstance(response, list):
            self._logger.error(f"Response to request recent results is not a list, but it is a {type(response)}")
            return []

        test_infos = []
        for single_test_info in response:
            try:
                test_infos.append(TestInfo.from_json(single_test_info))
            except Exception as e:
                if not isinstance(single_test_info, dict):
                    self._logger.warning(f"Cannot create TestInfo from instance of type {type(single_test_info)}")
                else:
                    self._logger.warning(f"Cannot create TestInfo from {single_test_info}")
        return test_infos


    def get_result_by_id(self, test_id: int) -> Dict:
        response = self.make_request(f"{self._test_result_path}/{test_id}", params={})
        if not isinstance(response, dict):
            self._logger.warning(f"Cannot use instance of type {type(response)} as test result")
            raise ValueError(response)
        if 'test_id' not in response:
            response['test_id'] = test_id
        return response


    _test_info_path: str
    _test_result_path: str
