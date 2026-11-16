
from chunking import (
    tokenize_by_sentences,
    tokenize_by_words,
    chunk_fixed_size,
    chunk_document,
)


def test_tokenize_by_sentences():
    text = "Первое предложение. Второе предложение! Третье предложение?"
    assert tokenize_by_sentences(text) == [
        "Первое предложение.",
        "Второе предложение!",
        "Третье предложение?",
    ]


def test_tokenize_by_words():
    assert tokenize_by_words("один   два три") == ["один", "два", "три"]


def test_chunk_fixed_size():
    tokens = ["один", "два", "три", "четыре", "пять"]
    assert chunk_fixed_size(tokens, chunk_size=3) == [
        ["один", "два", "три"],
        ["четыре", "пять"],
    ]


def test_chunk_fixed_size_with_overlap():
    tokens = ["a", "b", "c", "d", "e"]
    assert chunk_fixed_size(tokens, chunk_size=3, overlap=1) == [
        ["a", "b", "c"],
        ["c", "d", "e"],
    ]


def test_chunk_fixed_size_invalid_size():
    try:
        chunk_fixed_size(["a", "b"], chunk_size=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка ValueError")


def test_chunk_document_by_words():
    result = chunk_document("один два три четыре", chunk_size=2)
    assert result == [["один", "два"], ["три", "четыре"]]


def test_chunk_document_by_sentences():
    result = chunk_document(
        "Первое. Второе. Третье.",
        chunk_size=2,
        strategy="sentences",
    )
    assert result == [["Первое.", "Второе."], ["Третье."]]

def test_chunk_fixed_size_invalid_overlap():
    try:
        chunk_fixed_size(["a", "b", "c"], chunk_size=3, overlap=3)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка ValueError")

def test_chunk_fixed_size_empty_list():
    assert chunk_fixed_size([], chunk_size=3) == []


def test_chunk_fixed_size_last_chunk_is_shorter():
    tokens = ["a", "b", "c", "d"]
    assert chunk_fixed_size(tokens, chunk_size=3) == [
        ["a", "b", "c"],
        ["d"],
    ]


def test_chunk_fixed_size_negative_overlap():
    try:
        chunk_fixed_size(["a", "b"], chunk_size=3, overlap=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка ValueError")