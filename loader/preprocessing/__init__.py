from loader.preprocessing.categorial_fields_encoders import (
    BurnoutCategorialFieldsEncoder,
    DistressCategorialFieldsEncoder,
    CopingCategorialFieldsEncoder,
    SpbCategorialFieldsEncoder,
)
from loader.preprocessing.coping_respondent_age_gender_injector import CopingRespondentAgeGenderInjector
from loader.preprocessing.coping_t_score_calculator import CopingTScoreCalculator
from loader.preprocessing.pipeline import Pipeline
from loader.preprocessing.processor import Processor
from loader.preprocessing.relative_scores_injectors import (
    BurnoutRelativeScoreInjector,
    DistressRelativeScoreInjector,
)
from loader.preprocessing.test_result_fields_renamers import *
from loader.preprocessing.timestamp_to_datetime_recoder import TimestampToDatetimeRecoder
