import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from loader.storage import TestResult


class SpbTestRecord(TestResult):
    __tablename__ = "spb_results"

    test_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(nullable=True)
    respondent_id: Mapped[int]
    date_time: Mapped[datetime.datetime]

    catastrophization: Mapped[int]
    catastrophization_c: Mapped[int]

    due_to_self: Mapped[int]
    due_to_self_c: Mapped[int]

    due_to_others: Mapped[int]
    due_to_others_c: Mapped[int]

    low_frustration_tolerance: Mapped[int]
    low_frustration_tolerance_c: Mapped[int]

    selfestimation: Mapped[int]
    selfestimation_c: Mapped[int]

    def __repr__(self) -> str:
        return f"SpbTestRecord(test_id={self.test_id})"
