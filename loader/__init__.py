import sqlite3

from loader.errors import StorageError
from loader.gform_loader import load_gform_results
from loader.model import define_table, insert_result, InterviewResult
from loader.xls_loader import load_xls_result


def append_to_db(filename: str, result: InterviewResult):
    try:
        connection = create_database(filename)
    except sqlite3.OperationalError as e:
        raise StorageError(f"SQL error: {e}")
    except sqlite3.DatabaseError as e:
        raise StorageError(f"DB backend error: {e}")
    except Exception as e:
        raise StorageError(f"Unknown db error: {e}")
    cursor = connection.cursor()
    try:
        sql_statement = insert_result(result)
        cursor.execute(sql_statement)
        connection.commit()
    except sqlite3.OperationalError as e:
        raise StorageError(f"SQL error: {e}")
    except sqlite3.DatabaseError as e:
        raise StorageError(f"DB backend error: {e}")
    except Exception as e:
        raise StorageError(f"Unknown db error: {e}")


def create_database(filename: str) -> sqlite3.Connection:
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    sql_statement = define_table()
    cursor.execute(sql_statement)
    connection.commit()
    return connection
