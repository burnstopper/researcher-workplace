from pathlib import Path

import sqlalchemy

from loader.storage import TestResult


class LocalStorage:
    """This class is a holder of instantiated sqlalchemy sqlite engine"""
    def __init__(self, file_path: Path):
        """Creates new instance of LocalStorage.
        
        Arguments:
        file_path - path where the local storage db is located or should be created."""
        self.__file_path = file_path
        self.__engine = None


    def setup(self):
        """Initializes sqlalchemy engine.
        
        If sqlite db is not exist, the new one is created.
        If some table is missing, is is created.

        Note: remember that if the table exists and schema version of db does not match the schema version of loader
        the behaviour of loader might be unpredictable and can damage the data in local storage.
        """
        self.__create_engine()
        TestResult.metadata.create_all(self.engine)


    @property
    def engine(self) -> sqlalchemy.Engine:
        return self.__engine


    __engine: sqlalchemy.Engine
    __file_path: Path
    

    def __create_engine(self):
        db_uri = 'sqlite:///' + str(self.__file_path)
        self.__engine = sqlalchemy.create_engine(db_uri)
