import logging
from typing import List

from loader.preprocessing.errors import *
from loader.preprocessing.processor import Processor


class AbstractSinglePassProcessor(Processor):
    def __init__(self, test_name: str, processor_name: str):
        super().__init__(test_name)
        self._logger = logging.getLogger("loader.preprocessing")
        self._processor_name = processor_name


    def process(self, records: List) -> List:
        self._logger.info(f"Running {self._processor_name} of {self.test_name} results")
        len_before_processing = len(records)
        for ind, rec in enumerate(records):
            if not isinstance(rec, dict):
                raise RecordIsNotDict(self.test_name, ind)
            try:
                self._process_single_record_inplace(rec)
            except KeyError as e:
                name = e.args[0] if len(e.args) > 0 else "<not specified>"
                raise MissingResultValue(self.test_name, name)
        self._logger.debug(f"{len_before_processing} of {self.test_name} results processed with {self._processor_name}"
                           f" and result contains {len(records)} records")
        return records


    _processor_name: str


    def _process_single_record_inplace(self, record: dict) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}._process_single_record_inplace is not implemented")
