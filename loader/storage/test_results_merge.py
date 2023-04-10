import datetime

from sqlalchemy import text

from loader.storage import *


_SQL_IMPLEMENTATION = \
"""
WITH
	b AS (SELECT
		CAST(strftime('%s', date_time) AS INT) / (7 * 24 * 60 * 60) as week_number, MAX(date_time) as b_date_time, *
	FROM
		burnout_results
	WHERE date_time > :date_time
	GROUP BY respondent_id, week_number),
	c AS (SELECT
		CAST(strftime('%s', date_time) AS INT) / (7 * 24 * 60 * 60) as week_number, MAX(date_time) as c_date_time, *
	FROM
		coping_results
	WHERE date_time > :date_time
	GROUP BY respondent_id, week_number),
	d AS (SELECT
		CAST(strftime('%s', date_time) AS INT) / (7 * 24 * 60 * 60) as week_number, MAX(date_time) as d_date_time, *
	FROM
		distress_results
	WHERE date_time > :date_time
	GROUP BY respondent_id, week_number),
	s AS (SELECT
		CAST(strftime('%s', date_time) AS INT) / (7 * 24 * 60 * 60) as week_number, MAX(date_time) as s_date_time, *
	FROM
		spb_results
	WHERE date_time > :date_time
	GROUP BY respondent_id, week_number)
INSERT INTO results
SELECT
    b.respondent_id,
    MIN(b.date_time, c.date_time, d.date_time, s.date_time) as date_time,
    COALESCE(CASE WHEN b.quiz_id == c.quiz_id AND b.quiz_id = d.quiz_id AND b.quiz_id = s.quiz_id
        THEN 'quiz_' || CAST(b.quiz_id AS TEXT)
        ELSE NULL END, '') as key_source,
-- age is not supported now
    0,
-- age_c is not supported now
    0,
-- gender is not supported now
    'm',
-- position is not supported now
    'unknown',
-- jobs_num is currently not supported
    1,
-- experience is not supported now
    1,
    CASE WHEN b.quiz_id == c.quiz_id AND b.quiz_id = d.quiz_id AND b.quiz_id = s.quiz_id
        THEN b.quiz_id
        ELSE NULL END as quiz_id,
    d.distress,
    d.distress_p,
    d.distress_c,
    d.physical_discomfort,
    d.physical_discomfort_p,
    d.cognitive_discomfort,
    d.cognitive_discomfort_p,
    d.ea_violation,
    d.ea_violation_p,
    d.motivation_decrease,
    d.motivation_decrease_p,
    b.emotional_exhaustion,
    b.emotional_exhaustion_p,
    b.emotional_exhaustion_c,
    b.depersonalization,
    b.depersonalization_p,
    b.depersonalization_c,
    b.reduction_of_professionalism,
    b.reduction_of_professionalism_p,
    b.reduction_of_professionalism_c,
    b.burnout_p,
    b.burnout_index,
    b.burnout_index_p,
    c.confrontation,
    c.confrontation_c,
    c.distancing,
    c.distancing_c,
    c.selfcontrol,
    c.selfcontrol_c,
    c.seeking_social_support,
    c.seeking_social_support_c,
    c.taking_responsibility,
    c.taking_responsibility_c,
    c.escaping,
    c.escaping_c,
    c.problem_solving_planning,
    c.problem_solving_planning_c,
    c.positive_revaluation,
    c.positive_revaluation_c,
    s.catastrophization,
    s.catastrophization_c,
    s.due_to_self,
    s.due_to_self_c,
    s.due_to_others,
    s.due_to_others_c,
    s.low_frustration_tolerance,
    s.low_frustration_tolerance_c,
    s.selfestimation,
    s.selfestimation_c,
    '0.3'
FROM b
INNER JOIN c ON b.respondent_id = c.respondent_id AND b.week_number = c.week_number
INNER JOIN d ON b.respondent_id = d.respondent_id AND b.week_number = d.week_number
INNER JOIN s ON b.respondent_id = s.respondent_id AND b.week_number = s.week_number
ON CONFLICT (respondent_id, date_time) DO NOTHING;
"""


class TestResultsMerge:
    __test__ = False


    def __init__(self, since: datetime.datetime, storage: LocalStorage) -> None:
        self._storage = storage
        self._since = since


    def run(self):
        with self._storage.engine.connect() as con:
            stmt = text(_SQL_IMPLEMENTATION)
            con.execute(stmt, {'date_time': self._since.strftime('%Y-%m-%d %H:%M:%S')})
