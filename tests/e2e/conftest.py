import logging
from pathlib import Path

import pytest


# See pytest documentation to learn the bultin tmp_path fixture.
@pytest.fixture(scope="function")
def loader_config(tmp_path: Path):
    storage_path = tmp_path / "db.sqlite"
    config = {
        'burnout_service': '194.67.126.160:8080',
        'distress_service': '194.67.126.160:8081',
        'coping_service': '194.67.126.160:8082',
        'spb_service': '194.67.126.160:8083',
        'respondent_service': 'unknown',
        'kraepelin_service': '194.67.78.127:80',
        'token': 'ycK0pFhS6akv',
        'distress_token': 'qwertyRES',
        'db_path': storage_path
    }
    return config


# See pytest documentation to learn the builtin caplog fixture.
@pytest.fixture(autouse=True)
def verbose_logs_for_e2e_fixtures(caplog):
    caplog.set_level(logging.DEBUG, logger="loader")


@pytest.fixture(scope="session")
def source_gform_tables_dir() -> Path:
    return Path.cwd() / "tests" / "e2e" / "tests_data" / "gform"


@pytest.fixture(scope="session")
def source_xls_tables_dir() -> Path:
    return Path.cwd() / "tests" / "e2e" / "tests_data" / "xls"
