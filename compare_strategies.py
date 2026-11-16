
import json
from pathlib import Path

from chunking import chunk_document


DATA_DIR = Path(__file__).parent / "data"
RESULTS_DIR = Path(__file__).parent / "results"
INPUT_FILE = DATA_DIR / "cleaned_documents.txt"

SENTENCE_CHUNK_SIZE = 5
SENTENCE_OVERLAP = 1

WORD_CHUNK_SIZE = 100
WORD_OVERLAP = 10


def count_sentence_boundary_breaks(chunks):
    """Считает внутренние границы чанков, проходящие внутри предложения."""
    return sum(
        1
        for chunk in chunks[:-1]
        if chunk and not str(chunk[-1]).rstrip().endswith((".", "!", "?"))
    )


def calculate_metrics(chunks, strategy, chunk_size, overlap, unit):
    """Вычисляет количественные и структурные метрики чанков."""
    word_sizes = []

    for chunk in chunks:
        if unit == "sentences":
            word_sizes.append(
                sum(len(sentence.split()) for sentence in chunk)
            )
        else:
            word_sizes.append(len(chunk))

    chunk_count = len(chunks)
    boundary_breaks = count_sentence_boundary_breaks(chunks)

    return {
        "strategy": strategy,
        "unit": unit,
        "chunk_count": chunk_count,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "average_words_per_chunk": round(
            sum(word_sizes) / chunk_count, 2
        ) if chunk_count else 0,
        "min_words_per_chunk": min(word_sizes) if word_sizes else 0,
        "max_words_per_chunk": max(word_sizes) if word_sizes else 0,
        "sentence_boundary_breaks": boundary_breaks,
        "sentence_boundary_break_rate": round(
            boundary_breaks / (chunk_count - 1) * 100, 2
        ) if chunk_count > 1 else 0,
    }


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    chunks_a = chunk_document(
        text,
        chunk_size=SENTENCE_CHUNK_SIZE,
        overlap=SENTENCE_OVERLAP,
        strategy="sentences",
    )

    chunks_b = chunk_document(
        text,
        chunk_size=WORD_CHUNK_SIZE,
        overlap=WORD_OVERLAP,
        strategy="words",
    )

    results_a = {
        "metrics": calculate_metrics(
            chunks_a,
            "sentences",
            SENTENCE_CHUNK_SIZE,
            SENTENCE_OVERLAP,
            "sentences",
        ),
        "chunks": chunks_a,
    }

    results_b = {
        "metrics": calculate_metrics(
            chunks_b,
            "words",
            WORD_CHUNK_SIZE,
            WORD_OVERLAP,
            "words",
        ),
        "chunks": chunks_b,
    }

    (RESULTS_DIR / "strategy_A.json").write_text(
        json.dumps(results_a, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (RESULTS_DIR / "strategy_B.json").write_text(
        json.dumps(results_b, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("Сравнение стратегий разбиения")
    print("-" * 83)
    print(
        f"{'Метрика':<35}"
        f"{'Strategy A':>23}"
        f"{'Strategy B':>23}"
    )
    print("-" * 83)

    metric_labels = [
        ("chunk_count", "Количество чанков"),
        ("average_words_per_chunk", "Среднее слов в чанке"),
        ("min_words_per_chunk", "Минимум слов в чанке"),
        ("max_words_per_chunk", "Максимум слов в чанке"),
        ("sentence_boundary_breaks", "Разрывы предложений"),
        ("sentence_boundary_break_rate", "Доля разрывов, %"),
    ]

    for key, label in metric_labels:
        print(
            f"{label:<35}"
            f"{results_a['metrics'][key]:>23}"
            f"{results_b['metrics'][key]:>23}"
        )

    print("\nStrategy A — разбиение по предложениям.")
    print("Strategy B — разбиение по словам.")
    print("\nРезультаты сохранены:")
    print(RESULTS_DIR / "strategy_A.json")
    print(RESULTS_DIR / "strategy_B.json")
if __name__ == "__main__":
    main()
