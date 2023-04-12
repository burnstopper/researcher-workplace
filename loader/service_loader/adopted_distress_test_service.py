import datetime
from typing import Dict, List, Any

from loader.service_loader import TestInfo
from loader.service_loader.basic_rest_service import BasicRestService
from loader.service_loader.test_service import TestService


class AdoptedDistressTestService(TestService, BasicRestService):
    def __init__(self, host: str, port: int, token: str):
        BasicRestService.__init__(self, host, port, token)


    def get_recent_results(self, from_: datetime.datetime) -> List[TestInfo]:
        url = 'api/ihru/results'
        timestamp = int(from_.astimezone(TestService.TIMEZONE).timestamp())
        url_params = {'timestamp': timestamp}
        response = self.make_request(url, url_params)
        if isinstance(response, list):
            return self._parse_recent_results_response(response)
        else:
            raise ValueError(f"Expected response of type dict, but have: {type(response)}")


    def get_result_by_id(self, test_id: int) -> Dict:
        url = 'api/ihru'
        url_params = {'test_id': test_id}
        response = self.make_request(url, url_params)
        if isinstance(response, Dict):
            response['test_id'] = test_id
            AdoptedDistressTestService._do_consistency_renaming_of_test_results_field(response)
            return response
        else:
            raise ValueError(f"Expected response of type dict, but have: {type(response)}")


    def _parse_recent_results_response(self, response: List[dict]):
        return [self._parse_test_info(item) for item in response]


    def _parse_test_info(self, json) -> TestInfo:
        """TestInfo wants to see fields                'result_id', 'respondent_id', 'date_time', 'quiz_id'
        But currently ihru service response has fields 'test_id`,   'respondent_id', 'datetime',  'quiz_id'
        """
        json["date_time"] = json['datetime']
        json['result_id'] = json['test_id']
        return TestInfo.from_json(json)


    @staticmethod
    def _do_consistency_renaming_of_test_results_field(response: Dict[str, Any]) -> None:
        response["ea_violation"] = response["emotional_violation"]
        response.pop("emotional_violation")
        response["date_time"] = response["datetime"]
        response.pop("datetime")
