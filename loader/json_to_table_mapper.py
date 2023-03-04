from typing import Dict, Type
from loader.errors import MappingExistsError, MappingNotFoundError


class JsonToTableMapper:
    def __init__(self):
        self._test_name_to_table = dict()


    def register_mapping(self, test_name: str, table: Type):
        if test_name in self._test_name_to_table:
            raise MappingExistsError(test_name)
        self._test_name_to_table[test_name] = table


    def map_json(self, test_name: str, json: dict) -> object:
        if test_name not in self._test_name_to_table:
            raise MappingNotFoundError(test_name)
        obj_class = self._test_name_to_table[test_name]
        obj = obj_class()
        JsonToTableMapper._load_object_properties_from_json(obj, json)
        return obj


    _test_name_to_table: Dict[str, Type]


    @staticmethod
    def _load_object_properties_from_json(obj: object, json: dict):
        for key, value in json.items():
            setattr(obj, key, value)
