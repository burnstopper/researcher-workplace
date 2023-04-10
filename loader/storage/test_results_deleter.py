import datetime

from sqlalchemy import delete
from sqlalchemy.orm import Session

from loader.storage import *


class TestResultsDeleter:
    __test__ = False

    
    def __init__(self, since: datetime.datetime, storage: LocalStorage) -> None:
        self._storage = storage
        self._since = since

    def run(self):
        with Session(self._storage.engine) as session:
            for item in [ResultsTestRecord, BurnoutTestRecord, DistressTestRecord, CopingTestRecord, SpbTestRecord]:
                stmt = delete(item).where(item.date_time >= self._since)
                session.execute(stmt)
            session.commit()
