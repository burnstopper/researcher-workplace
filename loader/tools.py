from typing import Tuple

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


def distress_to_cat(x: int):
    if   x<=17: return 0
    elif x<=26: return 1
    elif x<=37: return 2
    elif x<=48: return 3
    else:       return 4


def emotional_exhaustion_to_cat(x: int):
    if x<=15:     return 0
    elif x<= 24:  return 1
    else:         return 2


def depersonalization_to_cat(x: int):
    if x<=5:      return 0
    elif x<= 10:  return 1
    else:         return 2
    

def reduction_of_professionalism_to_cat(x: int):
    if x>=37:     return 0
    elif x>30:    return 1
    else:         return 2


def spb_to_cat(x: int):
    if x<30:       return 2
    elif x<=45:    return 1
    else:          return 0


def lazarus_to_cat(x: int):
    if x<40:      return 0
    elif x<=60:   return 1
    else:         return 2


def expirience_to_int(x) -> int:
    try:
        return int(x)
    except ValueError:
        return 0


def get_service_host_and_port(service_endpoint: str) -> Tuple[str, int]:
    if ':' in service_endpoint:
        colon_pos = service_endpoint.find(':')
        host = service_endpoint[:colon_pos]
        port = int(service_endpoint[colon_pos + 1:])
    else:
        host = service_endpoint
        port = 443  # Using default tls port if it is not specified
    return host, port


def extract_service_token(service_name: str, config: dict) -> str:
    specific_name = service_name + '_token'
    common_name = 'token'  # Use common token as fallback

    if specific_name in config:
        return config[specific_name]
    else:
        return config[common_name]
