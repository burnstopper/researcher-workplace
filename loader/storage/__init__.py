from sqlalchemy.orm import DeclarativeBase


class TestResult(DeclarativeBase):
    __test__ = False  # Prohibit pytest usage of this class as unit test
    pass


from loader.storage.burnout_test_record import BurnoutTestRecord
from loader.storage.coping_test_record import CopingTestRecord
from loader.storage.distress_test_record import DistressTestRecord
from loader.storage.local_storage import LocalStorage
from loader.storage.results_test_record import ResultsTestRecord
from loader.storage.spb_test_record import SpbTestRecord
from loader.storage.test_results_deleter import TestResultsDeleter
from loader.storage.test_results_merge import TestResultsMerge


__all__ = [
    "BurnoutTestRecord",
    "DistressTestRecord",
    "CopingTestRecord",
    "SpbTestRecord",
    "LocalStorage",
    "TestResult",
    "ResultsTestRecord",
    "TestResultsDeleter",
    "TestResultsMerge",
]
