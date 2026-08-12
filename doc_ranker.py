from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable, List, Sequence


_TOKEN_PATTERN = re.compile(r"\b\w+\b")


def _tokenize(text: str) -> List[str]:
    return _TOKEN_PATTERN.findall(text.lower())


def rank_datasets(query: str, datasets: Sequence[str], top_k: int | None = None) -> List[dict]:
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    if top_k is not None and top_k < 1:
        raise ValueError("top_k must be >= 1 when provided")

    tokenized_docs = [_tokenize(dataset) for dataset in datasets]
    total_docs = len(tokenized_docs)
    if total_docs == 0:
        return []

    doc_freq = Counter()
    for tokens in tokenized_docs:
        doc_freq.update(set(tokens))

    query_tokens = _tokenize(query)
    if not query_tokens:
        ranked = [{"dataset": dataset, "score": 0.0} for dataset in datasets]
        return ranked[:top_k] if top_k else ranked

    query_term_counts = Counter(query_tokens)
    query_len = len(query_tokens)
    query_tfidf = {}
    for term, count in query_term_counts.items():
        tf = count / query_len
        idf = math.log((1 + total_docs) / (1 + doc_freq.get(term, 0))) + 1
        query_tfidf[term] = tf * idf

    ranked = []
    for dataset, tokens in zip(datasets, tokenized_docs):
        if not tokens:
            ranked.append({"dataset": dataset, "score": 0.0})
            continue

        doc_term_counts = Counter(tokens)
        doc_len = len(tokens)
        score = 0.0
        for term, q_weight in query_tfidf.items():
            tf = doc_term_counts.get(term, 0) / doc_len
            if tf == 0:
                continue
            idf = math.log((1 + total_docs) / (1 + doc_freq.get(term, 0))) + 1
            score += q_weight * (tf * idf)

        ranked.append({"dataset": dataset, "score": score})

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:top_k] if top_k else ranked
