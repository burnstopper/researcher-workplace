if [ -z "$VIRTUAL_ENV" ]
then
    . venv/bin/activate
fi

pytest -c pytest.ini --basetemp=./tests/tmp tests/e2e
