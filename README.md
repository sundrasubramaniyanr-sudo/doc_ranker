# doc_ranker
by using the TF-IDF algorithm the documents are ranked.

## Usage

```python
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
```
