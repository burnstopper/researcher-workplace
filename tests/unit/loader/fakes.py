import datetime
from typing import Any, Dict, List, Tuple

from loader.service_loader.test_service import *


class FakeTestService(TestService):
    def __init__(self):
        self._fake_results_registry = dict()


    _fake_results_registry: Dict[int, Tuple[TestInfo, Dict[str, Any]]]


    def add_test_results(self, payload: Dict[str, Any]):
        test_info = TestInfo.from_json(payload)
        self._fake_results_registry[test_info.test_id] = (test_info, payload)


    def get_recent_results(self, from_: datetime.datetime) -> List[TestInfo]:
        from_ = from_.astimezone(TestService.TIMEZONE)
        midnight = datetime.time(tzinfo=TestService.TIMEZONE)
        end_of_day = datetime.datetime.combine(from_.date(), midnight) + datetime.timedelta(hours=24)
        results = []
        for _, (ti, _) in self._fake_results_registry.items():
            ti: TestInfo
            filling_time = datetime.datetime.fromtimestamp(ti.date_time, TestService.TIMEZONE)
            if (from_ <= filling_time) and (filling_time < end_of_day):
                results.append(ti.copy())
        return results
    

    def get_result_by_id(self, test_id: int) -> Dict:
        return self._fake_results_registry[test_id][1]
