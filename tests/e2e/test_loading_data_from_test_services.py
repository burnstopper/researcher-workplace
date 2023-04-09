import datetime
import logging

from sqlalchemy.orm import Session

from loader import Loader
from loader.storage import *


class TestLoadDataFromTestServices:
    """This test loads all tests filled over last 7 days"""
    def test_main(self, loader_config: dict):
        logger = logging.getLogger("loader")
        ldr = Loader.from_config(loader_config)
        period = datetime.timedelta(days=7)
        stats = ldr.load_recent_results(period)
        logger.info(f"Downloaded {stats.number_of_downloaded_test_results}")
        with Session(ldr.storage.engine) as ses:
            number_of_records_in_db = 0
            number_of_records_in_db += ses.query(BurnoutTestRecord).count()
            number_of_records_in_db += ses.query(DistressTestRecord).count()
            number_of_records_in_db += ses.query(CopingTestRecord).count()
            number_of_records_in_db += ses.query(SpbTestRecord).count()
        assert stats.number_of_downloaded_test_results - stats.number_of_ignored_test_results == number_of_records_in_db
