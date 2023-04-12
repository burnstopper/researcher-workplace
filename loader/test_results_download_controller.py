import datetime
import logging
from typing import List

from loader.service_loader import TestInfo, TestService
from loader.service_loader.errors import ServiceError


class TestResultsDownloadController:
    __test__ = False


    def __init__(self, service: TestService):
        self._service = service
        self._logger = logging.getLogger(f"loader.{self.__class__.__name__}")


    def download_test_results(self, starting_date: datetime.date) -> List[dict]:
        self._logger.debug(f"Downloading tests result since {starting_date}")
        midnight = datetime.time(tzinfo=TestService.TIMEZONE)
        self._starting_date = datetime.datetime.combine(starting_date, midnight)
        self._today = datetime.datetime.combine(datetime.datetime.now(tz=TestService.TIMEZONE).date(), midnight)
        self._results = []
        self._tests_info = []
        self._download_tests_info()
        self._download_every_test_result()
        return self._results


    _service: TestService
    _starting_date: datetime.datetime
    _today: datetime.datetime
    _results: List[dict]
    _tests_info: List[TestInfo]
    

    def _download_tests_info(self) -> None:
        current_date = self._starting_date
        one_day_delta = datetime.timedelta(days=1)
        while current_date <= self._today:
            try:
                tests_info = self._service.get_recent_results(current_date)
                self._logger.debug(f"There are {len(tests_info)} tests in {current_date.date()}")
                self._tests_info.extend(tests_info)
            except ServiceError as e:
                self._logger.error(f"Failed to get list of tests at {current_date.date()}: {e}")
            current_date = current_date + one_day_delta


    def _download_every_test_result(self) -> None:
        for test_info in self._tests_info:
            result = self._service.get_result_by_id(test_info.test_id)
            self._results.append(result)
