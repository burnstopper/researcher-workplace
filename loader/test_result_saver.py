from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import inspect

from loader.storage import LocalStorage


class TestResultSaver:
    def __init__(self, storage: LocalStorage):
        self._storage = storage


    def save_results(self, test_results: List):
        num_of_inserted = 0
        with Session(self._storage.engine) as session:
            for result in test_results:
                dict_representation = TestResultSaver.convert_test_result_to_dict(result)
                statement = \
                    insert(result.__table__) \
                    .values(dict_representation) \
                    .on_conflict_do_nothing()
                result = session.execute(statement)
                num_of_inserted += result.rowcount
            session.commit()
        return num_of_inserted


    def save_or_replace(self, test_results: List):
        num_of_new_inserted = 0
        with Session(self._storage.engine) as session:
            for result in test_results:
                dict_representation = TestResultSaver.convert_test_result_to_dict(result)
                statement = \
                    insert(result.__table__) \
                    .values(dict_representation) \
                    .on_conflict_do_update(dict_representation)
                result = session.execute(statement)
                num_of_new_inserted += result.rowcount
            session.commit()
        return num_of_new_inserted


    @staticmethod
    def convert_test_result_to_dict(test_result):
        mapper = inspect(test_result).mapper
        result = dict()
        for attr_def in mapper.attrs:
            column_name = attr_def.key
            value = getattr(test_result, column_name, None)
            if value is not None:
                result[column_name] = value
        return result
