from loader.preprocessing.abstract_single_pass_processor import AbstractSinglePassProcessor
import loader.tools as tools


class BurnoutRelativeScoreInjector(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__("burnout", "relative score injector")


    def _process_single_record_inplace(self, record: dict):
        record["burnout_p"]  = BurnoutRelativeScoreInjector._calc_burnout_p(record)
        record["burnout_index_p"] = BurnoutRelativeScoreInjector._calc_burnout_index_p(record)
        record["emotional_exhaustion_p"] = record["emotional_exhaustion"] / tools.MAX_EMOTIONAL_EXHAUSTION
        record["depersonalization_p"] = record["depersonalization"] / tools.MAX_DEPERSONALIZATION
        record["reduction_of_professionalism_p"] = record["reduction_of_professionalism"] / tools.MAX_REDUCTION_OF_PROFESSIONALISM


    @staticmethod
    def _calc_burnout_p(record: dict) -> float:
        sum_ =  (record["emotional_exhaustion"] / tools.MAX_EMOTIONAL_EXHAUSTION) ** 2
        sum_ += (record["depersonalization"] / tools.MAX_DEPERSONALIZATION) ** 2
        sum_ += (1 - record["reduction_of_professionalism"] / tools.MAX_REDUCTION_OF_PROFESSIONALISM) ** 2
        sum_ /= 3
        sum_ = sum_ ** 0.5
        return sum_
    
    
    @staticmethod
    def _calc_burnout_index_p(record: dict) -> float:
        sum_ =  record["emotional_exhaustion"]
        sum_ += record["depersonalization"]
        sum_ += tools.MAX_REDUCTION_OF_PROFESSIONALISM - record["reduction_of_professionalism"]
        sum_ /= sum([tools.MAX_EMOTIONAL_EXHAUSTION, tools.MAX_DEPERSONALIZATION, tools.MAX_REDUCTION_OF_PROFESSIONALISM])
        return sum_


class DistressRelativeScoreInjector(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__("distress", "relative score injector")

    
    def _process_single_record_inplace(self, record: dict):
        names_and_max_vals = [
            ("distress", tools.MAX_DISTRESS),
            ("physical_discomfort", tools.MAX_PHYSICAL_DISCOMFORT),
            ("cognitive_discomfort", tools.MAX_PHYSICAL_DISCOMFORT),
            ("motivation_decrease", tools.MAX_DECREASE_MOTIVATION),
            ("ea_violation", tools.MAX_EA_VIOLATION)
        ]
        for name, max_val in names_and_max_vals:
            record[name + "_p"] = record[name] / max_val
