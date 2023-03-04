import datetime

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from loader.storage import TestResult


class ResultsTestRecord(TestResult):
    __tablename__ = "results"
    __table_args__ = (
        PrimaryKeyConstraint("respondent_id", "date_time", name="results_pk"),
    )

    respondent_id: Mapped[str]
    date_time: Mapped[datetime.datetime]
    key_source: Mapped[str]
    age: Mapped[str]
    age_c: Mapped[int]
    gender: Mapped[str]
    position: Mapped[str]
    jobs_num: Mapped[int]
    experience: Mapped[int]
    quiz_id: Mapped[int] = mapped_column(nullable=True)

    # Distress
    distress: Mapped[int]
    distress_p: Mapped[float]
    distress_c: Mapped[int]

    physical_discomfort: Mapped[int]
    physical_discomfort_p: Mapped[float]

    cognitive_discomfort: Mapped[int]
    cognitive_discomfort_p: Mapped[float]

    ea_violation: Mapped[int]
    ea_violation_p: Mapped[float]

    motivation_decrease: Mapped[float]
    motivation_decrease_p: Mapped[int]

   # Burnout
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

    # Coping
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

    # Spb
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

    schema_version: Mapped[str] = mapped_column(default="0.3")


    def __repr__(self) -> str:
        return f"Results(test_id={self.test_id})"
