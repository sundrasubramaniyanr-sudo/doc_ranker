import unittest

from doc_ranker import rank_datasets
from pathlib import Path

class RankDatasetsTests(unittest.TestCase):
    def test_ranks_most_relevant_dataset_first(self):
        data_dir = Path("IR_30dataset")
        datasets = []
        for file_path in sorted(data_dir.glob("*.txt")):
            datasets.append(file_path.read_text(encoding="utf-8").strip())

        results = rank_datasets("hitchcock", datasets)

        self.assertEqual(len(results), len(datasets))
        self.assertGreater(results[0]["score"], results[1]["score"])
        self.assertIn("dataset", results[0])

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
