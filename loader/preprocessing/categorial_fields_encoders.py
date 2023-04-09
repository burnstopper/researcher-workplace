import logging
from typing import List

from loader.preprocessing.abstract_single_pass_processor import AbstractSinglePassProcessor
from loader.preprocessing.errors import *
import loader.tools as tools


class BurnoutCategorialFieldsEncoder(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__('burnout', "categorial fields encoder")


    def _process_single_record_inplace(self, record: dict):
        for field_name in ['emotional_exhaustion', 'depersonalization', 'reduction_of_professionalism']:
            cat_field_name = field_name + '_c'
            record[cat_field_name] = tools.emotional_exhaustion_to_cat(record[field_name])


class DistressCategorialFieldsEncoder(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__('distress', "categorial fields encoder")
    
    
    def _process_single_record_inplace(self, record: dict):
        record['distress_c'] = tools.distress_to_cat(record['distress'])


class CopingCategorialFieldsEncoder(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__('coping', "categorial fields encoder")


    def _process_single_record_inplace(self, record: dict):
        for field_name in \
                        [
                            "confrontation",
                            "distancing",
                            "selfcontrol",
                            "seeking_social_support",
                            "taking_responsibility",
                            "escaping",
                            "problem_solving_planning",
                            "positive_revaluation"
                        ]:
            t_score = record[field_name + "_t"]
            cat_field_name = field_name + "_c"
            record[cat_field_name] = tools.lazarus_to_cat(t_score)


class SpbCategorialFieldsEncoder(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__('spb', "categorial fields encoder")


    def _process_single_record_inplace(self, record: dict):
        for field_name in \
                        [
                            "catastrophization",
                            "due_to_self",
                            "due_to_others",
                            "low_frustration_tolerance",
                            "selfestimation",
                        ]:
            cat_field_name = field_name + "_c"
            record[cat_field_name] = tools.spb_to_cat(record[field_name])
