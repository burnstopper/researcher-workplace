from typing import List

import pandas as pd

from loader.model import InterviewResult

def load_results_from_gform_results(file_path: str, key: str) -> List[InterviewResult]:
    try:
        df = pd.read_excel(file_path, sheet_name="Sheet1")
    except Exception as e:
        print(e)
    df.apply(lambda r: parse_interview_result(r, key), axis=1)


def create_respondent_id(key, row_number, age, expirience, timestamp):
    return f"{key}/{row_number}/{age}/{expirience}/{timestamp}"


def parse_interview_result(row, key: str):
    resp_id = create_respondent_id(key, row.name, row['age'], row[5], row[1])
    r = InterviewResult(resp_id, source=key)

