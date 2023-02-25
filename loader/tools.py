from datetime import date as Date

from pandas import Timestamp


MAX_DISTRESS = 72
MAX_COGNITIVE_DISCOMFORT = 20
MAX_PHYSICAL_DISCOMFORT = 30
MAX_EA_VIOLATION = 12
MAX_DECREASE_MOTIVATION = 10

MAX_EMOTIONAL_EXHAUSTION = 54
MAX_DEPERSONALIZATION = 30
MAX_REDUCTION_OF_PROFESSIONALISM = 48


def timestamp_to_date(tstamp: Timestamp):
    return Date(tstamp.year, tstamp.month, tstamp.day)


def recode_gender(value: str):
    if value == 'женский' or value == 'Женский':
        return 'f'
    if value == 'мужской' or value == 'Мужской':
        return 'm'
    raise ValueError("Failed to recode age")


def encode_age_cat(value: str):
    if '20' in value:
        return 0
    elif '21' in value:
        return 1
    elif '31' in value:
        return 2
    else:
        return 3


def distress_to_cat(x):
    if   x<=17: return 0
    elif x<=26: return 1
    elif x<=37: return 2
    elif x<=48: return 3
    else:       return 4


def emotional_exhaustion_to_cat(x):
    if x<=15:     return 0
    elif x<= 24:  return 1
    else:         return 2


def depersonalization_to_cat(x):
    if x<=5:      return 0
    elif x<= 10:  return 1
    else:         return 2
    

def reduction_of_professionalism_to_cat(x):
    if x>=37:     return 0
    elif x>30:    return 1
    else:         return 2


def spb_to_cat(x):
    if x<30:       return 2
    elif x<=45:    return 1
    else:          return 0


def lazarus_to_cat(x):
    if x<40:      return 0
    elif x<=60:   return 1
    else:         return 2
