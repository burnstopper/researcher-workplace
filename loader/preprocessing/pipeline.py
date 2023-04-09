from typing import List

from loader.preprocessing.errors import EmptyPreprocessingPipeline
from loader.preprocessing.processor import Processor


class Pipeline(Processor):
    def __init__(self, *processors):
        if len(processors) == 0:
            raise EmptyPreprocessingPipeline()
        for p in processors:
            if not isinstance(p, Processor):
                raise ValueError("Every argument of Pipeline.__init__() must be instance of Processor")
        super().__init__(processors[0].test_name)
        self._processors = list(processors)


    _processors: List[Processor]


    def process(self, records: List) -> List:
        for p in self._processors:
            records = p.process(records)
        return records
