from app import main, Result


def test_non_determinent_mode():
    args = [
        "argv0_is_not_important",
        "-d", "/dummy_path",
        "-o", "/dummy_path/db.sqlite",
        "--xls",
        "--gform",
        "-k", "cli",
    ]
    result = main(args)
    assert result == Result.BAD_ARGUMENTS


def test_not_selected_mode():
    args = [
        "argv0_is_not_important",
        "-d", "/dummy_path",
        "-o", "/dummpy_path/db.sqlite",
        "-k", "cli",
    ]
    result = main(args)
    assert result == Result.BAD_ARGUMENTS


def test_no_source():
    args = [
        "argv0_is_not_important",
        "-o", "/dummpy_path/db.sqlite",
        "-k", "cli",
        "--xls"
    ]
    result = main(args)
    assert result == Result.BAD_ARGUMENTS
