import logging

import pytest


@pytest.fixture(autouse=True)
def logs_for_unit_tests(caplog):
    caplog.set_level(logging.INFO, logger="loader")
