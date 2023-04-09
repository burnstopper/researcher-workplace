
class GFormLoadingError(Exception):
    pass

class LazarusKeysLoadingError(Exception):
    pass


class StorageError(Exception):
    pass


class MappingExistsError(Exception):
    def __init__(self, test_name: str):
        self.test_name = test_name
        message = f"Mapping for test {test_name} is already registered"
        super().__init__(self, message)


class MappingNotFoundError(Exception):
    def __init__(self, test_name: str):
        self.test_name = test_name
        message = f"Mapping for test {test_name} is not found"
        super().__init__(self, message)


class BadConfig(Exception):
    def __init__(self, property_name: str, *, missing=False, misconfigured=False):
        super().__init__()
        if missing:
            self._message = f"Missing config property: {property_name}"
            self._property_name = property_name
        elif misconfigured:
            self._message = f"Misconfigured config property {property_name}"
            self._property_name = property_name
        else:
            self._message = f"Generic configuration error"


    @property
    def property_name(self):
        return self._property_name


    def __str__(self):
        return self._message
