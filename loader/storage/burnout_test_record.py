import datetime

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from loader.storage import TestResult


class BurnoutTestRecord(TestResult):
    __tablename__ = "burnout_results"

    test_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(nullable=True)
    respondent_id: Mapped[int]
    date_time: Mapped[datetime.datetime]

    emotional_exhaustion: Mapped[int]
    emotional_exhaustion_p: Mapped[float]
    emotional_exhaustion_c: Mapped[int]

    depersonalization: Mapped[int]
    depersonalization_p: Mapped[float]
    depersonalization_c: Mapped[int]

    reduction_of_professionalism: Mapped[int]
    reduction_of_professionalism_p: Mapped[float]
    reduction_of_professionalism_c: Mapped[int]

    burnout_p: Mapped[float]
    burnout_index: Mapped[int]
    burnout_index_p: Mapped[float]

    def __repr__(self) -> str:
        return f"BurnoutTestRecord(test_id={self.test_id})"
