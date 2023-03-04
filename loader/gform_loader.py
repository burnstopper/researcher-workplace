import datetime as dt
from typing import List

import pandas as pd

from loader.coping_calc_table import load_coping_calc_table
from loader.errors import GFormLoadingError
from loader.storage import ResultsTestRecord
from loader.tools import *


SHEET_NAME = "Form Responses 1"


def load_gform_results(file_path: str, key: str) -> List[ResultsTestRecord]:
    try:
        df = pd.read_excel(file_path, sheet_name=SHEET_NAME)
    except Exception as e:
        raise GFormLoadingError(f"Loading sheet <{SHEET_NAME}> from file <{file_path}> failed", e)
    calc_distress_results(df)
    calc_burnout_results(df)
    calc_lazarus_results(df)
    calc_spb_results(df)
    return build_results(df, key)


def create_respondent_id(key, row_number, age, expirience, timestamp):
    return f"{key}/{row_number}/{age}/{expirience}/{timestamp}"


def append_column(df: pd.DataFrame, name: str, values: pd.Series):
    df.insert(df.shape[1], name, values)


#########################
# Processing distress
#########################
def distress_ans_to_score(x):
    return {
        'Да': 2,
        'Затрудняюсь ответить': 1,
        'Нет': 0
    }[x]


def calc_distress_results(df: pd.DataFrame):
    distress_df = df[df.columns[list(range(5, 41))]]
    distress_scores = distress_df.applymap(distress_ans_to_score)
    distress_neg_cols = distress_scores.columns[[0,5,13,21,32,35]]
    distress_scores[distress_neg_cols] = 2-distress_scores[distress_neg_cols]
    distress = distress_scores.apply(sum,1)

    physical_discomfort_cols = distress_scores.columns[[2,8,9,10,12,15,16,22,23,24,25,26,28,30,31,]]
    physical_discomfort = distress_scores[physical_discomfort_cols].apply(sum,1)

    cognitive_discomfort_cols = distress_scores.columns[[0,3,4,7,18,19,20,33,34,35,]]
    cognitive_discomfort = distress_scores[cognitive_discomfort_cols].apply(sum,1)

    emotional_violations_cols = distress_scores.columns[[1,6,14,17,21,29,]]
    emotional_violations = distress_scores[emotional_violations_cols].apply(sum,1)

    motivation_decrease_cols = distress_scores.columns[[5,11,13,27,32,]]
    motivation_decrease = distress_scores[motivation_decrease_cols].apply(sum,1)

    distress_cat = distress.apply(distress_to_cat)
    
    append_column(df, "distress", distress)
    append_column(df, "distress_p", distress / MAX_DISTRESS)
    append_column(df, "distress_c", distress_cat)
    append_column(df, "physical_discomfort", physical_discomfort)
    append_column(df, "physical_discomfort_p", physical_discomfort / MAX_PHYSICAL_DISCOMFORT)
    append_column(df, "cognitive_discomfort", cognitive_discomfort)
    append_column(df, "cognitive_discomfort_p", cognitive_discomfort / MAX_COGNITIVE_DISCOMFORT)
    append_column(df, "motivation_decrease", motivation_decrease)
    append_column(df, "motivation_decrease_p", motivation_decrease / MAX_DECREASE_MOTIVATION)
    append_column(df, "ea_violation", emotional_violations)
    append_column(df, "ea_violation_p", emotional_violations / MAX_EA_VIOLATION)


#######################
# Processing burnout
#######################
def burnout_to_score(x):
    return {
        'Никогда':0,
        'Очень редко':1,
        'Редко':2,
        'Иногда':3, 
        'Часто':4,
        'Очень часто':5,
        'Ежедневно':6
    }[x]


def calc_burnout_results(df: pd.DataFrame):
    burnout_df = df[df.columns[list(range(41, 63))]]
    burnout_score = burnout_df.applymap(burnout_to_score)
    burnout_neg_cols = burnout_score.columns[[5]]
    burnout_score[burnout_neg_cols] = 6-burnout_score[burnout_neg_cols]

    emotional_exhaustion_cols = burnout_score.columns[[0,1,2,5,7,12,13,15,19,]]
    emotional_exhaustion = burnout_score[emotional_exhaustion_cols].apply(sum,1)

    depersonalization_cols =burnout_score.columns[[4,9,10,14,21,]]
    depersonalization = burnout_score[depersonalization_cols].apply(sum,1)

    reduction_of_professionalism_cols = burnout_score.columns[[3,6,8,11,16,17,18,20,]]
    reduction_of_professionalism = burnout_score[reduction_of_professionalism_cols].apply(sum,1)

    emotional_exhaustion_cat = emotional_exhaustion.apply(emotional_exhaustion_to_cat)

    depersonalization_cat = depersonalization.apply(depersonalization_to_cat)
    
    reduction_of_professionalism_cat = reduction_of_professionalism.apply(reduction_of_professionalism_to_cat)

    burnout_p = \
    ((0
        + (emotional_exhaustion / MAX_EMOTIONAL_EXHAUSTION) ** 2 \
        + (depersonalization / MAX_DEPERSONALIZATION) ** 2 \
        + (1 - reduction_of_professionalism / MAX_REDUCTION_OF_PROFESSIONALISM) ** 2 \
    ) / 3) ** 0.5

    burnout_index = \
        emotional_exhaustion \
        + depersonalization \
        + MAX_REDUCTION_OF_PROFESSIONALISM \
        - reduction_of_professionalism

    burnout_index_p = burnout_index / (MAX_EMOTIONAL_EXHAUSTION + MAX_DEPERSONALIZATION + MAX_REDUCTION_OF_PROFESSIONALISM)

    append_column(df, "burnout_p", burnout_p)
    append_column(df, "burnout_index", burnout_index)
    append_column(df, "burnout_index_p", burnout_index_p)
    append_column(df, "emotional_exhaustion", emotional_exhaustion)
    append_column(df, "emotional_exhaustion_p", emotional_exhaustion / MAX_EMOTIONAL_EXHAUSTION)
    append_column(df, "emotional_exhaustion_c", emotional_exhaustion_cat)
    append_column(df, "depersonalization", depersonalization)
    append_column(df, "depersonalization_p", depersonalization / MAX_DEPERSONALIZATION)
    append_column(df, "depersonalization_c", depersonalization_cat)
    append_column(df, "reduction_of_professionalism", reduction_of_professionalism)
    append_column(df, "reduction_of_professionalism_p", reduction_of_professionalism / MAX_REDUCTION_OF_PROFESSIONALISM)
    append_column(df, "reduction_of_professionalism_c", reduction_of_professionalism_cat)


######################
# Processing Lazarus
######################
def coping_to_score(x):
    return {
        'Никогда':   0,
        'Редко':     1,
        'Иногда':    2,
        'Часто':     3,
    }[x]


def calc_lazarus_results(df: pd.DataFrame):
    coping_df = df[df.columns[63:113]]
    coping_score = coping_df.applymap(coping_to_score)
    sex_age = df[[df.columns[1], df.columns[2]]]
    sex_age.columns = ["sex", "age"]
    
    lazarus_list = [
        ['Конфронтация',                     [1,2,12,20,25,36],          'confrontation'],
        ['Дистанцирование',                  [7,8,10,15,31,34],          'distancing'],
        ['Самоконтроль',                     [5,9,26,33,43,48,49],       'selfcontrol'],
        ['Поиск социальной поддержки',       [3,13,16,23,32,35],         'seeking_social_support'],
        ['Принятие ответственности',         [4,18,21,41],               'taking_responsibility'],
        ['Бегство-избегание',                [6,11,24,30,37,40,45,46],   'escaping'],
        ['Планирование решения проблемы',    [0,19,29,38,39,42],         'problem_solving_planning'],
        ['Положительная переоценка',         [14,17,22,27,28,44,47],     'positive_revaluation'],
    ]
    t_scores = []

    for indicator, questions, _ in lazarus_list:
        indicator_cols = coping_score.columns[questions]
        indicator_score = coping_score[indicator_cols].apply(sum, 1)
        indicator_score.name = 'score'

        indicator_data = pd.concat([sex_age, indicator_score], axis=1)
        indicator_data['indicator'] = indicator
        
        indicator_data['sex'] = indicator_data['sex'].str.lower()
        
        indicator_data.loc[indicator_data['age'] == 'до 20 лет', ['age']] = 'До 20 лет'
        indicator_data.loc[indicator_data['age'] == '31-45 лет', ['age']] = 'от 31 до 45 лет'
        indicator_data.loc[indicator_data['age'] == '21-30 лет', ['age']] = 'от 21 до 30 лет'
        indicator_data.loc[indicator_data['age'] == '46-60 лет', ['age']] = 'от 46 до 60 лет'

        indicator_data.reset_index(drop=True, inplace=True)
        indicator_result = pd.merge(
            indicator_data,
            load_coping_calc_table(),
            how = 'left',
            on=['sex', 'age', 'score', 'indicator']
        )
        t_scores.append(indicator_result['t_score'])

    for t_score, (_, _, indicator_name) in zip(t_scores, lazarus_list):
        append_column(df, indicator_name, t_score)
        # indicator_text_value = t_score.apply(lazarus_to_text)
        indicator_cat_value = t_score.apply(lazarus_to_cat)
        # append_column(df, indicator_name + "_t", indicator_text_value)
        append_column(df, indicator_name + "_c", indicator_cat_value)


##########################
# Processing SPB
##########################
def spb_to_score(x):
    return {
        "Полностью согласен":       1,
        "В основном согласен":      2,
        "Слегка согласен":          3,
        "Слегка не согласен":       4,
        "В основном не согласен":   5,
        "Полностью не согласен":    6,
    }[x]


def calc_spb_results(df: pd.DataFrame):
    spb_df = df[df.columns[113:163]]

    spb_score = spb_df.applymap(spb_to_score)
    spb_neg_cols = spb_score.columns[[0,3,12,16,19,21,24,25,27,33,37,41,45,48]]
    spb_score[spb_neg_cols] = 7-spb_score[spb_neg_cols]

    catastrophization_cols = spb_score.columns[[0,5,10,15,20,25,30,35,40,45]]
    catastrophization = spb_score[catastrophization_cols].apply(sum,1)

    duty_to_oneself_cols = spb_score.columns[[1,6,11,16,21,26,31,36,41,46]]
    duty_to_oneself = spb_score[duty_to_oneself_cols].apply(sum,1)

    due_in_relation_to_others_cols = spb_score.columns[[2,7,12,17,22,27,32,37,42,47]]
    due_in_relation_to_others = spb_score[due_in_relation_to_others_cols].apply(sum,1)

    low_frustration_tolerance_cols = spb_score.columns[[3,8,13,18,23,28,33,38,43,48]]
    low_frustration_tolerance = spb_score[low_frustration_tolerance_cols].apply(sum,1)

    selfestimation_cols = spb_score.columns[[4,9,14,19,24,29,34,39,44,49]]
    selfestimation = spb_score[selfestimation_cols].apply(sum,1)

    for spb_val,spb_vname in [
        (catastrophization,'catastrophization'),
        (duty_to_oneself,'due_to_self'),
        (due_in_relation_to_others,'due_to_others'),
        (low_frustration_tolerance,'low_frustration_tolerance'),
        (selfestimation,'selfestimation'),
    ]:
        append_column(df, spb_vname, spb_val)
        append_column(df, f'{spb_vname}_c', spb_val.apply(spb_to_cat))


def build_results(df: pd.DataFrame, key: str) -> List[ResultsTestRecord]:
    df['date_time'] = df['Timestamp'].apply(lambda x: x - dt.timedelta(microseconds=x.microsecond))
    df['gender'] = df['Пол'].apply(recode_gender)
    df['position'] = df['Специальность ']
    df['age'] = df['Возраст (полных лет)']
    df['age_c'] = df['age'].apply(encode_age_cat)
    df['experience'] = df['Сколько лет вы учитесь/работаете в ИТ?'].apply(expirience_to_int)
    results = []
    for index, row in df.iterrows():
        timestamp = int(row.loc['date_time'].timestamp())
        sex = row.loc['gender']
        age  = row.loc['age']
        expirience = row.loc['experience']
        respondent_id = create_respondent_id(key, index, age, expirience, timestamp)
        record = ResultsTestRecord()
        record.respondent_id = respondent_id
        record.key_source = key
        record.gender = sex
        for col in df.columns:
            setattr(record, col, row[col])
        record.jobs_num = 0
        results.append(record)
    return results
