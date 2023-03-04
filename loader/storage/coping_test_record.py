import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from loader.storage import TestResult


class CopingTestRecord(TestResult):
    __tablename__ = "coping_results"

    test_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(nullable=True)
    respondent_id: Mapped[int]
    date_time: Mapped[datetime.datetime]

    confrontation: Mapped[int]
    confrontation_c: Mapped[int]
    
    distancing: Mapped[int]
    distancing_c: Mapped[int]
    
    selfcontrol: Mapped[int]
    selfcontrol_c: Mapped[int]
    
    seeking_social_support: Mapped[int]
    seeking_social_support_c: Mapped[int]
    
    taking_responsibility: Mapped[int]
    taking_responsibility_c: Mapped[int]
    
    escaping: Mapped[int]
    escaping_c: Mapped[int]
    
    problem_solving_planning: Mapped[int]
    problem_solving_planning_c: Mapped[int]
    
    positive_revaluation: Mapped[int]
    positive_revaluation_c: Mapped[int]

    def __repr__(self) -> str:
        return f"CopingTestRecord(test_id={self.test_id})"
