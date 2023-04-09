from sqlalchemy.orm import DeclarativeBase


class TestResult(DeclarativeBase):
    __test__ = False  # Prohibit pytest usage of this class as unit test
    pass


from loader.storage.burnout_test_record import BurnoutTestRecord
from loader.storage.distress_test_record import DistressTestRecord
from loader.storage.coping_test_record import CopingTestRecord
from loader.storage.spb_test_record import SpbTestRecord
from loader.storage.results_test_record import ResultsTestRecord
from loader.storage.local_storage import LocalStorage


__all__ = [
    "BurnoutTestRecord",
    "DistressTestRecord",
    "CopingTestRecord",
    "SpbTestRecord",
    "LocalStorage",
    "TestResult",
    "ResultsTestRecord",
]
