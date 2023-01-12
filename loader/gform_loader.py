from typing import List

import pandas as pd

from loader.model import InterviewResult
from loader.errors import GFormLoadingError

SHEET_NAME = "Form Responses 1"

def load_gform_results(file_path: str, key: str) -> List[InterviewResult]:
    try:
        df = pd.read_excel(file_path, sheet_name=SHEET_NAME)
    except Exception as e:
        raise GFormLoadingError(f"Loading sheet <{SHEET_NAME}> from file <{file_path}> failed", e)
    calc_distress_results(df)
    return df


def create_respondent_id(key, row_number, age, expirience, timestamp):
    return f"{key}/{row_number}/{age}/{expirience}/{timestamp}"


def parse_interview_result(row, key: str):
    resp_id = create_respondent_id(key, row.name, row['age'], row[5], row[1])
    r = InterviewResult(resp_id, source=key)


def append_column(df: pd.DataFrame, name: str, values: pd.Series):
    df.insert(df.shape[1], name, values)


#########################
# Processing distress
#########################
MAX_DISTRESS = 72
MAX_COGNITIVE_DISCOMFORT = 20
MAX_PHYSICAL_DISCOMFORT = 30
MAX_EA_VIOLATION = 12
MAX_DECREASE_MOTIVATION = 10


def distress_ans_to_score(x):
    return {
        'Да': 2,
        'Затрудняюсь ответить': 1,
        'Нет': 0
    }[x]


def distress_to_text(x):
    if   x<=17: return "Отсутствие признаков хронического утомления"
    elif x<=26: return "Начальная степень хронического утомления"
    elif x<=37: return "Выраженная степень хронического утомления"
    elif x<=48: return "Сильная степень хронического утомления"
    else:       return "Переход в область патологических состояний (астенический синдром)"


def distress_to_cat(x):
    if   x<=17: return 0
    elif x<=26: return 1
    elif x<=37: return 2
    elif x<=48: return 3
    else:       return 4


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

    distress_text = distress.apply(distress_to_text)
    distress_cat = distress.apply(distress_to_cat)
    
    append_column(df, "distress", distress)
    append_column(df, "distress_p", distress / MAX_DISTRESS)
    append_column(df, "distress_t", distress_text)
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
MAX_EMOTIONAL_EXHAUSTION = 54
MAX_DEPERSONALIZATION = 30
MAX_REDUCTION_OF_PROFESSIONALISM = 48


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


def emotional_exhaustion_to_text(x):
    if x<=15:     return "Низкий уровень"
    elif x<= 24:  return "Средний уровень"
    else:         return "Высокий уровень"


def emotional_exhaustion_to_cat(x):
    if x<=15:     return 0
    elif x<= 24:  return 1
    else:         return 2


def depersonalization_to_text(x):
    if x<=5:      return "Низкий уровень"
    elif x<= 10:  return "Средний уровень"
    else:         return "Высокий уровень"


def depersonalization_to_cat(x):
    if x<=5:      return 0
    elif x<= 10:  return 1
    else:         return 2
    

def reduction_of_professionalism_to_text(x):
    if x>=37:     return "Низкий уровень"
    elif x>30:    return "Средний уровень"
    else:         return "Высокий уровень"


def reduction_of_professionalism_to_cat(x):
    if x>=37:     return 0
    elif x>30:    return 1
    else:         return 2


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

    emotional_exhaustion_text = emotional_exhaustion.apply(emotional_exhaustion_to_text)
    emotional_exhaustion_cat = emotional_exhaustion.apply(emotional_exhaustion_to_cat)

    depersonalization_text = depersonalization.apply(depersonalization_to_text)
    depersonalization_cat = depersonalization.apply(depersonalization_to_cat)
    
    reduction_of_professionalism_text = reduction_of_professionalism.apply(reduction_of_professionalism_to_text)
    reduction_of_professionalism_cat = reduction_of_professionalism.apply(reduction_of_professionalism_to_cat)

    burnout_p = \
    ((0
        + (emotional_exhaustion / MAX_EMOTIONAL_EXHAUSTION) ** 2 \
        + (depersonalization / MAX_DEPERSONALIZATION) ** 2 \
        + (1 - reduction_of_professionalism / MAX_REDUCTION_OF_PROFESSIONALISM) ** 2 \
    ) / 3) ** 0.5

    append_column(df, "burnout_p", burnout_p)
    append_column(df, "emotional_exhaustion", emotional_exhaustion)
    append_column(df, "emotional_exhaustion_p", emotional_exhaustion / MAX_EMOTIONAL_EXHAUSTION)
    append_column(df, "emotional_exhaustion_t", emotional_exhaustion_text)
    append_column(df, "emotional_exhasution_c", emotional_exhaustion_cat)
    append_column(df, "depersonalization", depersonalization)
    append_column(df, "depersonalization_p", depersonalization / MAX_DEPERSONALIZATION)
    append_column(df, "depersonalization_t", depersonalization_text)
    append_column(df, "depersonalization_c", depersonalization_cat)
    append_column(df, "reduction_of_professionalism", reduction_of_professionalism)
    append_column(df, "reduction_of_professionalism_p", reduction_of_professionalism / MAX_REDUCTION_OF_PROFESSIONALISM)
    append_column(df, "reduction_of_professionalism_t", reduction_of_professionalism_text)
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


def lazarus_to_cat(x):
    if x<40:      return 0
    elif x<=60:   return 1
    else:         return 2


def lazarus_to_text(x):
    return {
        0: "Редкое использование стратегии",
        1: "Умеренное использование стратегии",
        2: "Выраженное предпочтение стратегии",
    }[lazarus_to_cat(x)]


def calc_lazarus_results(df: pd.DataFrame):
    coping_df = df[df.columns[63:113]]
    coping_score = coping_df.applymap(coping_to_score)
    sexage = df[[1, 2]]

    lazarus_list = [
        ['Конфронтация',                     [1,2,12,20,25,36],          'Confrontation'],
        ['Дистанцирование',                  [7,8,10,15,31,34],          'Distancing'],
        ['Самоконтроль',                     [5,9,26,33,43,48,49],       'Self-control'],
        ['Поиск социальной поддержки',       [3,13,16,23,32,35],         'Seeking social support'],
        ['Принятие ответственности',         [4,18,21,41],               'Taking responsibility'],
        ['Бегство-избегание',                [6,11,24,30,37,40,45,46],   'Escape-avoidance'],
        ['Планирование решения проблемы',    [0,19,29,38,39,42],         'Problem solving planning'],
        ['Положительная переоценка',         [14,17,22,27,28,44,47],     'Positive reassessment'],
    ]
    lazarus_t = []
    lazarus_k = []
    lazarus_v = []

    for indicator,questions,_ in lazarus_list:
        ind_cols = coping_score.columns[questions]
        ind_mark = coping_score[ind_cols].apply(sum,1)
        ind_mark.name = 'mark'
        ind_data = pd.concat([sexage,ind_mark],axis=1)
        ind_data['indicator'] = indicator
        ind_data2 = pd.merge(
            ind_data,
            t_data,
            how = 'left',
            left_on = ['sex', 'age', 'mark', 'indicator'],
            right_on = ['пол', 'возраст', 'сырой балл', 'шкала']
            )
        ind_t = ind_data2['Т-балл']
        ind_text = ind_t.apply(lazarus_to_text)
        ind_cat = ind_t.apply(lazarus_to_cat)
        lazarus_t.append(ind_t)
        lazarus_k.append(ind_text)
        lazarus_v.append(ind_cat)

    for laz_t, laz_k, laz_v, laz_list in zip(lazarus_t, lazarus_k, lazarus_v, lazarus_list):
        ind_name = laz_list[-1]
        append_column(df, ind_name, laz_t)
        append_column(df, ind_name + "_t", laz_k)
        append_column(df, ind_name + "_c", laz_v)
