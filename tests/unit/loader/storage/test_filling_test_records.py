import datetime
from pathlib import Path

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loader.storage import *


@pytest.fixture(scope="function")
def local_storage() -> LocalStorage:
    storage = LocalStorage(Path(":memory:"))
    storage.setup()
    return storage


def test_smoke_test(local_storage):
    pass


def test_insert_valid_burnout(local_storage: LocalStorage):
    r = BurnoutTestRecord()
    r.burnout_index = 10
    r.burnout_index_p = 0.1
    r.burnout_p = 0.2
    r.depersonalization = 10
    r.depersonalization_p = 0.1
    r.depersonalization_c = 2
    r.reduction_of_professionalism = 10
    r.reduction_of_professionalism_c = 3
    r.reduction_of_professionalism_p = 0.6
    r.emotional_exhaustion = 14
    r.emotional_exhaustion_c = 1
    r.emotional_exhaustion_p = 0.4
    r.date_time = datetime.datetime.now()
    r.quiz_id = 123
    r.test_id = 123
    r.respondent_id = 123
    with Session(local_storage.engine) as session:
        session.add(r)
        session.commit()


def test_insert_valid_distress(local_storage: LocalStorage):
    r = DistressTestRecord()
    r.test_id = 3
    r.respondent_id = 5
    r.date_time = datetime.datetime.now()
    r.distress = 7
    r.distress_p = 0.4
    r.distress_c = 0
    r.physical_discomfort = 7
    r.physical_discomfort_p = 0.83
    r.cognitive_discomfort = 22
    r.cognitive_discomfort_p = 0.16
    r.ea_violation = 13
    r.ea_violation_p = 0.2
    r.motivation_decrease = 4
    r.motivation_decrease_p = 0.1
    with Session(local_storage.engine) as session:
        session.add(r)
        session.commit()


def test_insert_valid_coping(local_storage: LocalStorage):
    r = CopingTestRecord()
    r.test_id = 92
    r.respondent_id = 18
    r.date_time = datetime.datetime.now()
    r.confrontation = 17
    r.confrontation_c = 3
    r.distancing = 52
    r.distancing_c = 2
    r.selfcontrol = 50
    r.selfcontrol_c = 1
    r.seeking_social_support = 32
    r.seeking_social_support_c = 2
    r.taking_responsibility = 44
    r.taking_responsibility_c = 3
    r.escaping = 21
    r.escaping_c = 1
    r.problem_solving_planning = 10
    r.problem_solving_planning_c = 0
    r.positive_revaluation = 60
    r.positive_revaluation_c = 4
    with Session(local_storage.engine) as session:
        session.add(r)
        session.commit()


def test_insert_valid_spb(local_storage: LocalStorage):
    r = SpbTestRecord()
    r.test_id = 92
    r.respondent_id = 18
    r.date_time = datetime.datetime.now()
    r.catastrophization = 17
    r.catastrophization_c = 3
    r.due_to_others = 11
    r.due_to_others_c = 1
    r.due_to_self = 7
    r.due_to_self_c = 0
    r.low_frustration_tolerance = 5
    r.low_frustration_tolerance_c = 3
    r.selfestimation = 7
    r.selfestimation_c = 0
    with Session(local_storage.engine) as session:
        session.add(r)
        session.commit()


@pytest.mark.parametrize("record_type", [BurnoutTestRecord, DistressTestRecord, CopingTestRecord, SpbTestRecord])
def test_insert_invalid(local_storage: LocalStorage, record_type):
    record = record_type()
    record.test_id = 10
    with pytest.raises(IntegrityError):
        with Session(local_storage.engine) as session:
            session.add(record)
            session.commit()
