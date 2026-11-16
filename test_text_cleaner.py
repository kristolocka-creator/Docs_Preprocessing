import pytest

from text_cleaner import (
    normalize_whitespace,
    remove_special_characters,
    normalize_case,
    clean_text,
)


def test_normalize_whitespace():
    assert normalize_whitespace("  Hello   world  ") == "Hello world"


def test_normalize_whitespace_empty_string():
    assert normalize_whitespace("") == ""


def test_remove_special_characters():
    assert remove_special_characters("Hello @world #2026!") == "Hello world 2026!"


def test_remove_special_characters_without_punctuation():
    assert remove_special_characters("Hello, world!", keep_punctuation=False) == "Hello world"


def test_remove_special_characters_keeps_hyphen():
    assert remove_special_characters("state-of-the-art") == "state-of-the-art"


def test_remove_special_characters_only_special_characters():
    assert remove_special_characters("@#$%") == ""


def test_normalize_case():
    assert normalize_case("HeLLo WoRLD") == "hello world"


def test_normalize_case_without_lower():
    assert normalize_case("HeLLo WoRLD", lower=False) == "HeLLo WoRLD"


def test_clean_text():
    assert clean_text("  HELLO   @WORLD!!!  ") == "hello world!!!"


def test_clean_text_with_options():
    assert clean_text(
        "  HELLO   @WORLD!!!  ",
        keep_punctuation=False,
        lower=False,
    ) == "HELLO WORLD"


def test_clean_text_empty_string():
    assert clean_text("") == ""


def test_clean_text_only_special_characters():
    assert clean_text("@#$%") == ""
