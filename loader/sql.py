SCHEMA_VERSION = '1.0.0'

DEFINE_TABLE = \
"""
CREATE TABLE IF NOT EXISTS results(
    respondent_id VARCHAR NOT NULL,
    date DATE NOT NULL,
    ihru INTEGER,
    phy_discomfort INTEGER,
    cog_discomfort INTEGER,
    ea_violation INTEGER,
    motivation_dec INTEGER,
    emotional_exhaustion INTEGER,
    depersonalization INTEGER,
    prof_reduction INTEGER,
    burnout_index REAL,
    confronation INTEGER,
    distancing INTEGER,
    selfcontrol INTEGER,
    soc_sup_search INTEGER,
    responsibility_taking INTEGER,
    escaping INTEGER,
    problem_solving_planning INTEGER,
    positive_revaluation INTEGER,
    obligation_to_self INTEGER,
    obligation_to_others INTEGER,
    frustration_tolerance INTEGER,
    selfesteem INTEGER,
    schema_version VARCHAR,
    PRIMARY KEY(respondent_id, date)
)
"""

APPEND_ROW = \
f"""
INSERT OR IGNORE INTO results
VALUES(
    :id,
    :date,
    :ihru,
    :phy_discomfort,
    :cog_discomfort,
    :ea_violation,
    :motivation_dec,
    :emotional_exhaustion,
    :depersonalization,
    :prof_reduction,
    :burnout_index,
    :confrontation,
    :distancing,
    :selfcontrol,
    :soc_sup_search,
    :responsibility_taking,
    :escaping,
    :problem_solving_planning,
    :positive_revaluation,
    :obligation_to_self,
    :obligation_to_others,
    :frustration_tolerance,
    :selfesteem,
    '{SCHEMA_VERSION}'
)
"""
