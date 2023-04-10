import datetime
import logging
import sqlite3
from typing import Any, Dict

from loader.errors import StorageError
from loader.gform_loader import load_gform_results
from loader.json_to_table_mapper import JsonToTableMapper
from loader.service_loader import TestService
from loader.storage import *
from loader.test_implementation_holder import TestImplementationFactory, TestImplementationHolder
from loader.test_result_saver import TestResultSaver
from loader.xls_loader import load_xls_result


def append_to_db(storage: LocalStorage, result: ResultsTestRecord):
    saver = TestResultSaver(storage)
    try:
        saver.save_results([result])
    except sqlite3.OperationalError as e:
        raise StorageError(f"SQL error: {e}")
    except sqlite3.DatabaseError as e:
        raise StorageError(f"DB backend error: {e}")
    except Exception as e:
        raise StorageError(f"Unknown db error: {e}")


class LoadingResultsStatistics:
    number_of_downloaded_test_results: int
    number_of_new_test_results: int
    number_of_ignored_test_results: int


    def __init__(self):
        self.number_of_downloaded_test_results = 0
        self.number_of_new_test_results = 0
        self.number_of_ignored_test_results = 0


class Loader:
    @staticmethod
    def from_config(config: dict) -> 'Loader':
        ldr = Loader()
        ldr._config = config.copy()
        ldr._initialize()
        return ldr


    def load_recent_results(self, period: datetime.timedelta = datetime.timedelta(days=1)) -> LoadingResultsStatistics:
        """The function tries to load results from all mciroservices.
        
        Results already existing in local storage are ignored.

        Arguments:
        period - the period of interest for which results are loaded.
        """
        stats = LoadingResultsStatistics()
        starting_date = (datetime.datetime.now(TestService.TIMEZONE) - period).date()
        for test_name, holder in self._test_holders.items():
            test_results = holder.download_controller.download_test_results(starting_date)
            processed_results = holder.preprocessing_pipeline.process(test_results)
            mapped_results = [self._json_mapper.map_json(test_name, t) for t in processed_results]

            num_downloaded = len(test_results)
            num_saved = self._saver.save_results(mapped_results)
            stats.number_of_downloaded_test_results += len(test_results)
            stats.number_of_ignored_test_results += num_downloaded - num_saved
            stats.number_of_new_test_results += num_saved
        return stats
    

    def reload_results(self, since: datetime.datetime) -> LoadingResultsStatistics:
        """The function deletes all results with date_time < since and tries to load new results from all microservices.
        
        Arguments:
        since - the instance of datetime.datetime which represents the point in the past from wich results are reloaded.
        """
        TestResultsDeleter(since, self.storage).run()
        return self.load_recent_results(datetime.datetime.now(since.tzinfo) - since)


    def merge_results(self) -> None:
        """The function tries to move all data independent tables individual for every microservice to a common results
        table.
        """
        date_time = ResultsTestRecord.get_last_record_date_time(self.storage)
        TestResultsMerge(date_time, self.storage).run()


    @property
    def storage(self) -> LocalStorage:
        """This property should only be used if existing API is not enough."""
        return self._storage


    _config: Dict[str, Any]
    _test_holders: Dict[str, TestImplementationHolder]
    _storage: LocalStorage
    _saver: TestResultSaver
    _json_mapper: JsonToTableMapper


    def _initialize(self):
        self._logger = logging.getLogger("loader")
        self._json_mapper = JsonToTableMapper()
        self._storage = LocalStorage(self._config['db_path'])
        self._storage.setup()
        self._saver = TestResultSaver(self._storage)
        self._init_test_implementation_holders()


    def _init_test_implementation_holders(self):
        self._test_holders = dict()
        factory = TestImplementationFactory()
        services_list = filter(lambda x: x.endswith("_service"), self._config.keys())
        test_names = [item[:len(item) - len("_service")] for item in services_list]
        for test_name in test_names:
            holder = factory.create(test_name, self._config)
            if not holder:
                self._logger.warning(f"Test {test_name} is not currenlty supported")
                continue
            self._test_holders[test_name] = holder
            self._json_mapper.register_mapping(test_name, holder.test_result_record)
