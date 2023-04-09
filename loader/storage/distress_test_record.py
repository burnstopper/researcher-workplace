import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from loader.storage import TestResult


class DistressTestRecord(TestResult):
    __tablename__ = "distress_results"

    test_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(nullable=True)
    respondent_id: Mapped[int]
    date_time: Mapped[datetime.datetime]

    distress: Mapped[int]
    distress_p: Mapped[float]
    distress_c: Mapped[int]

    physical_discomfort: Mapped[int]
    physical_discomfort_p: Mapped[float]

    cognitive_discomfort: Mapped[int]
    cognitive_discomfort_p: Mapped[float]

    ea_violation: Mapped[int]
    ea_violation_p: Mapped[float]

    motivation_decrease: Mapped[int]
    motivation_decrease_p: Mapped[float]

    def __repr__(self) -> str:
        return f"DistressTestRecord(test_id={self.test_id})"
