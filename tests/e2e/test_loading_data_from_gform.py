from pathlib import Path
from typing import Any, Dict

from sqlalchemy.orm import Session

from app import main, Result
from loader.storage import LocalStorage, ResultsTestRecord


def test_loading_data_from_gform(loader_config: Dict[str, Any],
                                 source_gform_tables_dir: Path):
    db_storage = loader_config['db_path']
    args = [
        "argv0_is_not_important",
        "-f", str(source_gform_tables_dir / "gform_sample.xlsx"),
        "-o", str(db_storage),
        "--gform",
        "-k", "gform-tests",
    ]
    result = main(args)
    assert result == Result.SUCCESS
    storage = LocalStorage(db_storage)
    storage.setup()
    with Session(storage.engine) as session:
        number_or_records = session.query(ResultsTestRecord).count()
    assert number_or_records == 5
