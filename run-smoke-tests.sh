if [ -z "$VIRTUAL_ENV" ]
then
    . venv/bin/activate
fi

pytest -c pytest.ini tests --basetemp=./tests/tmp -k "smoke_test"
