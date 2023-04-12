import datetime

import pytest

from loader.test_results_download_controller import TestResultsDownloadController
from tests.unit.loader.fakes import FakeTestService


@pytest.fixture(scope="module")
def fake_service() -> FakeTestService:
    service = FakeTestService()
    service.add_test_results({
        "respondent_id": 12421,
        "date_time": 1675209600,  # 1 Feb 2023 00:00 UTC
        "burnout_score": 10,
        "quiz_id": 15,
        "result_id": 100
    })
    service.add_test_results({
        "respondent_id": 17,
        "date_time": 1675987200,  # 10 Feb 2023 00:00 UTC
        "burnout_score": 1,
        "quiz_id": 18,
        "result_id": 200
    })
    service.add_test_results({
        "respondent_id": 5,
        "date_time": 1896912000,  # 10 Feb 2030 00:00 UTC. The project, probably, will not live so long.
        "burnout_score": 6,
        "quiz_id": 20,
        "result_id": 300
    })
    return service


@pytest.fixture(scope="function")
def controller(fake_service: FakeTestService) -> TestResultsDownloadController:
    return TestResultsDownloadController(fake_service)


def test_downloading_only_two_really_existing(controller: TestResultsDownloadController):
    test_results = controller.download_test_results(datetime.datetime(2023, 2, 1))
    assert len(test_results) == 2
    assert test_results[0]["result_id"] == 100
    assert test_results[1]["result_id"] == 200


def test_downloading_existing_without_very_old(controller: TestResultsDownloadController):
    test_results = controller.download_test_results(datetime.datetime(2023, 2, 5))
    assert len(test_results) == 1
    assert test_results[0]["result_id"] == 200


def test_downloading_nothing_very_old(controller: TestResultsDownloadController):
    test_results = controller.download_test_results(datetime.datetime(2024, 1, 1))
    assert len(test_results) == 0
