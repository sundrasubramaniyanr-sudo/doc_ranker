from __future__ import annotations

import html
import math
import re
from collections import Counter
from pathlib import Path

TOKEN_PATTERN = re.compile(r"\b\w+\b")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def clean_html(text: str) -> str:
    return HTML_TAG_PATTERN.sub(" ", html.unescape(text))


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(clean_html(text).lower())


def rank_datasets(query: str, datasets: list[str], top_k: int | None = None) -> list[dict]:
    documents = [tokenize(document) for document in datasets]
    if not documents:
        return []

    document_frequency = Counter(
        term for document in documents for term in set(document)
    )
    total_documents = len(documents)

    def tfidf(tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        length = len(tokens)
        if length == 0:
            return {}

        return {
            term: (count / length)
            * (math.log((total_documents + 1) / (document_frequency[term] + 1)) + 1)
            for term, count in counts.items()
        }

    query_vector = tfidf(tokenize(query))
    query_norm = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))

    results = []
    for original_document, tokens in zip(datasets, documents):
        document_vector = tfidf(tokens)
        document_norm = math.sqrt(
            sum(weight ** 2 for weight in document_vector.values())
        )

        dot_product = sum(
            query_weight * document_vector.get(term, 0)
            for term, query_weight in query_vector.items()
        )
        score = (
            dot_product / (query_norm * document_norm)
            if query_norm and document_norm else 0.0
        )
        results.append(
            {
                "dataset": original_document,
                "document": original_document,
                "score": score,
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k] if top_k else results


def rank_dataset_directory(directory: str | Path, query: str, top_k: int | None = None):
    paths = sorted(Path(directory).glob("*.txt"))
    documents = [path.read_text(encoding="utf-8", errors="replace") for path in paths]

    ranked = rank_datasets(query, documents, top_k)
    for result in ranked:
        dataset_value = result.get("dataset", result.get("document"))
        index = documents.index(dataset_value)
        result["filename"] = paths[index].name

    return ranked


if __name__ == "__main__":
    query = input("Enter your search query: ").strip()
    results = rank_dataset_directory("IR_30dataset", query, top_k=10)

    for position, result in enumerate(results, start=1):
        print(f"{position}. {result['filename']} — score: {result['score']:.4f}")
