import unittest

from doc_ranker import rank_datasets
from pathlib import Path

class RankDatasetsTests(unittest.TestCase):
    def test_ranks_most_relevant_dataset_first(self):
        # 1. Define path to your dataset folder relative to this file
        data_dir = Path("IR_30datasets")

        # 2. Read each .txt file into the datasets list
        datasets = []
        for file_path in data_dir.glob("*.txt"):
            datasets.append(file_path.read_text(encoding="utf-8").strip())

        # 3. Proceed with query and test logic
        query = "python tfidf"
        
        # Example call to your ranking function:
        # results = rank_datasets(query, datasets)
        # self.assertEqual(results[0], "expected top document text")

        results = rank_datasets("tf idf ranking code", datasets)

        self.assertEqual(results[0]["dataset"], "python code ranking with tf idf")
        self.assertGreater(results[0]["score"], results[1]["score"])

    def test_top_k_limits_results(self):
        datasets = ["apple", "banana", "apple banana"]

        results = rank_datasets("apple", datasets, top_k=2)

        self.assertEqual(len(results), 2)

    def test_empty_query_returns_zero_scores(self):
        datasets = ["a", "b"]

        results = rank_datasets("", datasets)

        self.assertEqual(results[0]["score"], 0.0)
        self.assertEqual(results[1]["score"], 0.0)


if __name__ == "__main__":
    unittest.main()
