from datetime import date as Date
from typing import Type as PythonType


TABLE_NAME = "results"


class ColumnTypeError(Exception):
    def __init__(self, name: str, expected_type: PythonType, actual_type: PythonType):
        self.message = f"Attribute '{name}' should be value of type {expected_type}, but it is value of type {actual_type}"
        super().__init__(self.message)
        self.expected = expected_type
        self.actual = actual_type
        self.name = name


class UnmappedPythonTypeError(Exception):
    def __init__(self, name: str, type_: PythonType):
        self.message = f"Attribute {name} of type {type_} is not mapped to any SQLite type"
        super().__init__(self.message)
        self.column_name = name
        self.type = type_


class MissingAttributeError(Exception):
    def __init__(self, name: str):
        message = f"Attribute '{name}' not present for interview result"
        super().__init__(message)
        self.name = name


class InterviewResult:
    """This is DTO class without behaviour."""
    
    id: str
    date: Date
    source: str
    age: str
    age_c: int
    gender: str
    position: str
    experience: int
    jobs_num: int
    timestamp: int
    
    # Индекс хронического утомления
    distress: int
    distress_p: float
    distress_c: int
    
    # Симптомы физического дискомфорта
    physical_discomfort: int
    physical_discomfort_p: float
    
    # Снижение общего самочувствия и когнитивный дискомфорт
    cognitive_discomfort: int
    cognitive_discomfort_p: float
    
    # Нарушения в эмоционально-аффективной сфере
    ea_violation: int
    ea_violation_p: float
    
    # Снижение мотивации и изменения в сфере социального общения
    motivation_decrease: int
    motivation_decrease_p: float
    
    # Эмоциональное истощение 
    emotional_exhaustion: int
    emotional_exhaustion_p: float
    emotional_exhaustion_c: int
    
    # Деперсонализация
    depersonalization: int
    depersonalization_p: float
    depersonalization_c: int
    
    # Редукция профессионализма
    reduction_of_professionalism: int
    reduction_of_professionalism_p: float
    reduction_of_professionalism_c: int
    
    # Интегральный индекс выгорания
    burnout_p: float
    burnout_index: int
    burnout_index_p: float
    
    # Конфронтация
    confrontation: int
    confrontation_c: int
    
    # Дистанцирование
    distancing: int
    distancing_c: int
    
    # Самоконтроль
    selfcontrol: int
    selfcontrol_c: int
    
    # Поиск социальной поддержки
    seeking_social_support: int
    seeking_social_support_c: int
    
    # Принятие ответственности
    taking_responsibility: int
    taking_responsibility_c: int
    
    # Бегство-избегание
    escaping: int
    escaping_c: int
    
    # Планирование решения проблемы
    problem_solving_planning: int
    problem_solving_planning_c: int
    
    # Положительная переоценка
    positive_revaluation: int
    positive_revaluation_c: int
    
    # Катастрофизация
    catastrophization: int
    catastrophization_c: int
    
    # Долженствование в отношении себя
    due_to_self: int
    due_to_self_c: int
    
    # Долженствование в отношении других
    due_to_others: int
    due_to_others_c: int
    
    # Низкая фрустрационная толерантность
    low_frustration_tolerance: int
    low_frustration_tolerance_c: int
    
    # Самооценка
    selfestimation: int
    selfestimation_c: int
    
    # Версия кода
    schema_version: str


    def __init__(self, id: str, source: str):
        self.id = id
        self.source = source
        self.schema_version = '0.2'
        # TODO: may be in future it is worth to set up default 'None' values for known attributes.
        # Some validation can be implemented later.


    def __repr__(self):
        return f"<InterviewResult of '{self.id}' at {self.date}>"


    def __str__(self):
        res = dict()
        for key in dir(self):
            if key.startswith('_'):
                continue
            res[key] = getattr(self, key)
        return str(res)


def _type_mapper(name: str, type_: PythonType) -> str:
    if type_ is int:
        return 'INTEGER'
    elif type_ is float:
        return "REAL"
    elif type_ is Date:
        return "VARCHAR"
    elif type_ is str:
        return "VARCHAR"
    else:
        raise UnmappedPythonTypeError(name, type_)


def define_table() -> str:
    """Creates SQL statement to define the result table"""
    column_definitions = []
    d = InterviewResult.__annotations__
    for col_name in d.keys():
        if col_name.startswith("_"):
            continue
        expected_type = d[col_name]
        sql_typename = _type_mapper(col_name, expected_type)
        column_definitions.append(f"{col_name} {sql_typename}")
    table_definition = \
        "CREATE TABLE IF NOT EXISTS results(" + \
        ", ".join(column_definitions) + \
        ");"
    return table_definition


def insert_result(ir: InterviewResult) -> str:
    """Appends new result to existing table"""
    annotations = InterviewResult.__annotations__
    attributes = ir.__dict__
    column_name_list = []
    values_list = []
    for col_name in annotations:
        if col_name.startswith("_"):
            continue
        if col_name not in attributes:
            raise MissingAttributeError(col_name)
        value = attributes[col_name]
        expected_attr_type = annotations[col_name]
        actual_attr_type = type(value)
        if type(attributes[col_name]) is not annotations[col_name]:
            raise ColumnTypeError(col_name, expected_attr_type, actual_attr_type)
        column_name_list.append(col_name)
        if actual_attr_type is int or actual_attr_type is float:
            value = str(value)
        else:
            value = "'" + str(value) + "'"
        values_list.append(value)

    result = \
        f"INSERT INTO {TABLE_NAME} (" + \
        ", ".join(column_name_list) + \
        ") VALUES (" + \
        ", ".join(values_list) + \
        ");"
    return result
