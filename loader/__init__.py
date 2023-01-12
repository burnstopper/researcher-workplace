import sqlite3

from loader.model import InterviewResult
from loader.sql import(
    DEFINE_TABLE as SQL_DEFINE_TABLE,
    APPEND_ROW as SQL_APPEND_ROW
)
from loader.xls_loader import load_result
from loader.gform_loader import load_gform_results


class StorageError(Exception):
    pass


def append_to_db(filename: str, result: InterviewResult):
    try:
        connection = create_database(filename)
    except sqlite3.DatabaseError as e:
        raise StorageError(f"DB error: {e}")
    except Exception as e:
        raise StorageError(f"Internal db error: {e}")
    cursor = connection.cursor()
    try:
        cursor.execute(SQL_APPEND_ROW, result.__dict__)
        connection.commit()
    except sqlite3.OperationalError as e:
        raise StorageError(f"SQL error: {e}")
    except sqlite3.DatabaseError as e:
        raise StorageError(f"DB error: {e}")
    except Exception as e:
        raise StorageError(f"Internal db error: {e}")


def create_database(filename: str) -> sqlite3.Connection:
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    res = cursor.execute(SQL_DEFINE_TABLE)
    connection.commit()
    return connection
