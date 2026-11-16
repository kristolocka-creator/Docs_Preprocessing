
import re


def tokenize_by_sentences(text):
    """Разбивает текст на предложения."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [sentence for sentence in sentences if sentence]


def tokenize_by_words(text):
    """Разбивает текст на отдельные слова."""
    return text.split()



def chunk_fixed_size(tokens, chunk_size, overlap=0):
    """Разбивает последовательность токенов на чанки заданного размера."""
    if chunk_size <= 0:
        raise ValueError("chunk_size должен быть больше 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap должен быть неотрицательным и меньше chunk_size"
        )

    chunks = []
    step = chunk_size - overlap
    start = 0

    while start < len(tokens):
        chunk = tokens[start:start + chunk_size]

        if not chunk:
            break

        chunks.append(chunk)

        # Если дошли до конца последовательности, останавливаемся.
        if start + chunk_size >= len(tokens):
            break

        start += step

    return chunks



def chunk_document(text, chunk_size=100, overlap=0, strategy="words"):
    """Разбивает документ на чанки по словам или предложениям."""
    if strategy == "words":
        tokens = tokenize_by_words(text)
    elif strategy == "sentences":
        tokens = tokenize_by_sentences(text)
    else:
        raise ValueError("strategy должна быть 'words' или 'sentences'")

    return chunk_fixed_size(tokens, chunk_size, overlap)
