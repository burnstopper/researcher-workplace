import pandas as pd

from loader.preprocessing.abstract_single_pass_processor import AbstractSinglePassProcessor
from loader.coping_calc_table import load_coping_calc_table


class CopingTScoreCalculator(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__("coping", "lazarus t_score calculator")
        self._table = load_coping_calc_table()
    
    
    _table: pd.DataFrame


    def _process_single_record_inplace(self, record: dict):
        gender_in_table = 'мужской' if record['gender'] == 'm' else 'женский'
        age_in_table = self._get_age_in_table(record['age'])
        for indicator_name, indicator_name_in_table in CopingTScoreCalculator._INDICATOR_NAMES_IN_TABLE.items():
            pd_index = (self._table['sex'] == gender_in_table)
            pd_index &= (self._table['age'] == age_in_table)
            pd_index &= (self._table['indicator'] == indicator_name_in_table)
            pd_index &= (self._table['score'] == record[indicator_name])
            t_score = self._table[pd_index].iloc[0]['t_score']
            record[indicator_name + '_t'] = t_score


    @staticmethod
    def _get_age_in_table(age: int):
        if age <= 20:
            return 'До 20 лет'
        elif 21 <= age <= 30:
            return 'от 21 до 30 лет'
        elif 31 <= age <= 45:
            return 'от 31 до 45 лет'
        else:
            return 'от 46 до 60 лет'


    _INDICATOR_NAMES_IN_TABLE = {
        "confrontation": "Конфронтация",
        "distancing": "Дистанцирование",
        "selfcontrol": "Самоконтроль",
        "seeking_social_support": "Поиск социальной поддержки",
        "taking_responsibility": "Принятие ответственности",
        "escaping": "Бегство-избегание",
        "problem_solving_planning": "Планирование решения проблемы",
        "positive_revaluation": "Положительная переоценка"
    }
