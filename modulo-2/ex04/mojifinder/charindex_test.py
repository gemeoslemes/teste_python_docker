import pytest
from charindex import tokenize, CharIndex


@pytest.mark.parametrize(
    "given, expected",
    [
        ("Hello world", ["HELLO", "WORLD"]),
        ("Testing 123", ["TESTING", "123"]),
        ("Special @#$ characters!", ["SPECIAL", "CHARACTERS"]),
        ("Mixed CASE text", ["MIXED", "CASE", "TEXT"]),
        ("hyphenated-word", ["HYPHENATED", "WORD"]),
        ("", []),  # Empty string case
        ("   ", []),  # Whitespace only
        ("123", ["123"]),  # Numbers only
        ("café", ["CAFÉ"]),  # Text with accents
        (
            "words_with_underscore",
            ["WORDS_WITH_UNDERSCORE"],
        ),  # Underscore is treated as part of word
    ],
)
def test_tokenize(given: str, expected: list[str]) -> None:
    """Test the tokenize function with various inputs."""
    result = tokenize(given)
    assert result == expected


@pytest.mark.parametrize(
    "label, given, expected",
    [
        ("single word", ["ASTERISK"], ["*"]),
        ("digits", ["DIGIT"], list("0123456789")),
        ("digit 8", ["DIGIT", "EIGHT"], ["8"]),
        ("less than", ["THAN", "LESS"], ["<"]),
        ("signs", ["SIGN"], ["#", "$", "%", "+", "<", "=", ">"]),
        ("no such character", ["NO_SUCH_CHARACTER"], []),
        ("empty query", [], []),
    ],
)
def test_search(label: str, given: list[str], expected: list[str]) -> None:
    ascii64 = CharIndex(0, 64)
    result = ascii64.search(given)
    assert result == expected, label
