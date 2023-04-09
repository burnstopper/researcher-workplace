class MissingResultValue(Exception):
    def __init__(self, test_name: str, name: str):
        super().__init__()
        self._test_name = test_name
        self._name = name

    def __str__(self):
        return f"Missing value '{self._name}' in results of test '{self._test_name}'"


    def __repr__(self):
        return f"MissingResultValue({self._test_name}, {self._name})"


class RecordIsNotDict(Exception):
    def __init__(self, test_name: str, record_index: int):
        super().__init__()
        self._test_name = test_name
        self._record_index = record_index


    def __str__(self):
        return f"Bad record type by index {self._record_index} of results from {self._test_name}, expected dict"
    

    def __repr__(self):
        return f"RecordIsNotDict({self._test_name}, {self._record_index})"


class EmptyPreprocessingPipeline(Exception):
    def __str__(self):
        return "Empty preprocessing pipline is not allowed"
