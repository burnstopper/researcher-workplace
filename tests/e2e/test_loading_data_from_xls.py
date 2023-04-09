from pathlib import Path
from typing import Any, Dict

from sqlalchemy.orm import Session

from app import main, Result
from loader.storage import LocalStorage, ResultsTestRecord


def test_loading_data_from_xls_file(loader_config: Dict[str, Any],
                                    source_xls_tables_dir: Path):
    db_storage = loader_config['db_path']
    args = [
        "argv0_is_not_important",
        "-f", str(source_xls_tables_dir / "Респондент 020.xlsx"),
        "-o", str(db_storage),
        "--xls",
        "-k", "xls-tests",
    ]
    result = main(args)
    assert result == Result.SUCCESS
    storage = LocalStorage(db_storage)
    storage.setup()
    with Session(storage.engine) as session:
        number_or_records = session.query(ResultsTestRecord.__table__).count()
    assert number_or_records == 1


def test_loading_data_from_xls_dir(loader_config: Dict[str, Any],
                                   source_xls_tables_dir: Path):
    db_storage = loader_config['db_path']
    args = [
        "argv0_is_not_important",
        "-d", str(source_xls_tables_dir),
        "-o", str(db_storage),
        "--xls",
        "-k", "xls-tests",
    ]
    result = main(args)
    assert result == Result.SUCCESS
    storage = LocalStorage(db_storage)
    storage.setup()
    with Session(storage.engine) as session:
        number_or_records = session.query(ResultsTestRecord.__table__).count()
    assert number_or_records == 2
