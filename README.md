# doc_ranker
by using the TF-IDF algorithm the documents are ranked.

## Usage

```python
from doc_ranker import rank_datasets

datasets = [
    "python code ranking with tf idf",
    "chocolate cake recipe",
]

results = rank_datasets("tf idf ranking", datasets)
print(results)
```
