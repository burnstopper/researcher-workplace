from datetime import date as Date


class InterviewResult:
    """This is DTO class without behaviour."""
    
    id: str
    date: Date
    age: int
    gender: str
    position: str
    experience: int
    jobs_num: int
    
    # ИХРУ
    ihru: int
    
    # Симптомы физического дискомфорта
    phy_discomfort: int
    
    # Снижение общего самочувствия и когнитивный дискомфорт
    cog_discomfort: int
    
    # Нарушения в эмоционально-аффективной сфере
    ea_violation: int
    
    # Снижение мотивации и изменения в сфере социального общения
    motivation_dec: int
    
    # Эмоциональное истощение 
    emotioanl_exhaustion: int
    
    # Деперсонализация
    depersonalization: int
    
    # Редукция профессионализма
    prof_reduction: int
    
    # Интегральный индекс выгорания
    burnout_index: float
    
    # Конфронтация
    confrontation: int
    
    # Дистанцирование
    distancing: int
    
    # Самоконтроль
    selfcontrol: int
    
    # Поиск социальной поддержки
    soc_sup_search: int
    
    # Принятие ответственности
    responsibility_taking: int
    
    # Бегство-избегание
    escaping: int
    
    # Планирование решения проблемы
    problem_solving_planning: int
    
    # Положительная переоценка
    positive_revaluation: int
    
    # Катастрофизация
    catastrophizing: int
    
    # Долженствование в отношении себя
    obligation_to_self: int
    
    # Долженствование в отношении других
    obligation_to_others: int
    
    # Низкая фрустрационная толерантность
    frustration_tolerance: int
    
    # Самооценка
    selfesteem: int
    

    def __init__(self, id: str):
        self.id = id
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
