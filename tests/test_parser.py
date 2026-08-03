from question_folder.parser import extract_key_result


def test_extracts_key_result() -> None:
    assert extract_key_result("Steps\nKey Result: 42") == "42"


def test_fallback() -> None:
    assert extract_key_result("First\nLast") == "Last"


def test_empty() -> None:
    assert extract_key_result("") == "N/A"
