from typing import List

class Processor:
    def __init__(self, test_name: str):
        self._test_name = test_name


    @property
    def test_name(self) -> str:
        return self._test_name


    def process(self, records: List) -> List:
        raise NotImplementedError("Processor.processor is not implemented")
