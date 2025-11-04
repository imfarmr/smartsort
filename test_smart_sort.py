import unittest
import random
from smart_sort import SmartSort, InputCharacteristics, SortStrategy


class TestInputCharacteristics(unittest.TestCase):
    
    def test_presortedness_fully_sorted(self):
        data = [1, 2, 3, 4, 5]
        chars = InputCharacteristics(data)
        self.assertGreater(chars.presortedness, 0.95)
    
    def test_presortedness_reverse_sorted(self):
        data = [5, 4, 3, 2, 1]
        chars = InputCharacteristics(data)
        self.assertLess(chars.presortedness, 0.1)
    
    def test_presortedness_nearly_sorted(self):
        data = [1, 2, 3, 5, 4, 6, 7]
        chars = InputCharacteristics(data)
        self.assertGreater(chars.presortedness, 0.7)
    
    def test_range_density_dense(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        chars = InputCharacteristics(data)
        self.assertGreater(chars.range_density, 0.9)
    
    def test_range_density_sparse(self):
        data = [1, 100, 200, 300, 400]
        chars = InputCharacteristics(data)
        self.assertLess(chars.range_density, 0.1)
    
    def test_distribution_uniform(self):
        data = [5, 5, 5, 5, 5]
        chars = InputCharacteristics(data)
        self.assertEqual(chars.distribution_type, "uniform")
    
    def test_duplicates_detection(self):
        data = [1, 2, 3, 2, 4]
        chars = InputCharacteristics(data)
        self.assertTrue(chars.has_duplicates)
    
    def test_no_duplicates(self):
        data = [1, 2, 3, 4, 5]
        chars = InputCharacteristics(data)
        self.assertFalse(chars.has_duplicates)


class TestSmartSort(unittest.TestCase):
    
    def setUp(self):
        self.sorter = SmartSort(verbose=False)
    
    def test_empty_array(self):
        data = []
        result = self.sorter.sort(data)
        self.assertEqual(result, [])
    
    def test_single_element(self):
        data = [42]
        result = self.sorter.sort(data)
        self.assertEqual(result, [42])
    
    def test_already_sorted(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.sorter.sort(data)
        self.assertEqual(result, data)
    
    def test_reverse_sorted(self):
        data = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_random_array(self):
        data = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
        expected = sorted(data)
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_duplicates(self):
        data = [5, 2, 8, 2, 9, 1, 5, 5]
        expected = sorted(data)
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_negative_numbers(self):
        data = [3, -1, 4, -5, 2, -3, 0]
        expected = sorted(data)
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_large_array(self):
        data = list(range(1000, 0, -1))
        expected = sorted(data)
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_nearly_sorted(self):
        data = [1, 2, 3, 4, 5, 7, 6, 8, 9, 10]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_small_range_dense(self):
        data = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0]
        expected = sorted(data)
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_original_unchanged(self):
        original = [5, 2, 8, 1, 9]
        data_copy = original.copy()
        self.sorter.sort(data_copy)
        self.assertEqual(original, [5, 2, 8, 1, 9])
    
    def test_statistics_tracking(self):
        data = [5, 2, 8, 1, 9]
        self.sorter.sort(data)
        stats = self.sorter.get_stats()
        
        self.assertIn("comparisons", stats)
        self.assertIn("swaps", stats)
        self.assertIn("strategy_switches", stats)
        self.assertIn("execution_time", stats)
        self.assertGreater(stats["comparisons"], 0)
        self.assertGreater(len(stats["strategy_switches"]), 0)


class TestAdaptiveStrategy(unittest.TestCase):
    
    def setUp(self):
        self.sorter = SmartSort(verbose=False)
    
    def test_insertion_sort_for_small_array(self):
        data = [5, 2, 8, 1, 9]
        self.sorter.sort(data)
        stats = self.sorter.get_stats()
        
        strategies = [s["strategy"] for s in stats["strategy_switches"]]
        self.assertIn(SortStrategy.INSERTION_SORT.value, strategies)
    
    def test_insertion_sort_for_nearly_sorted(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        self.sorter.sort(data)
        stats = self.sorter.get_stats()
        
        strategies = [s["strategy"] for s in stats["strategy_switches"]]
        self.assertIn(SortStrategy.INSERTION_SORT.value, strategies)
    
    def test_radix_sort_for_dense_range(self):
        data = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0] * 5
        self.sorter.sort(data)
        stats = self.sorter.get_stats()
        
        strategies = [s["strategy"] for s in stats["strategy_switches"]]
        self.assertIn(SortStrategy.RADIX_SORT.value, strategies)
    
    def test_merge_sort_for_random_large(self):
        random.seed(42)
        data = [random.randint(1, 10000) for _ in range(100)]
        self.sorter.sort(data)
        stats = self.sorter.get_stats()
        
        strategies = [s["strategy"] for s in stats["strategy_switches"]]
        self.assertIn(SortStrategy.MERGE_SORT.value, strategies)


class TestEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.sorter = SmartSort(verbose=False)
    
    def test_all_same_elements(self):
        data = [7, 7, 7, 7, 7, 7, 7]
        expected = [7, 7, 7, 7, 7, 7, 7]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_two_elements_sorted(self):
        data = [1, 2]
        expected = [1, 2]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_two_elements_unsorted(self):
        data = [2, 1]
        expected = [1, 2]
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_alternating_pattern(self):
        data = [1, 10, 2, 9, 3, 8, 4, 7, 5, 6]
        expected = sorted(data)
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)
    
    def test_large_numbers(self):
        data = [1000000, 500000, 750000, 250000, 875000]
        expected = sorted(data)
        result = self.sorter.sort(data)
        self.assertEqual(result, expected)


class TestPerformance(unittest.TestCase):
    
    def setUp(self):
        self.sorter = SmartSort(verbose=False)
    
    def test_performance_random_1000(self):
        random.seed(42)
        data = [random.randint(1, 10000) for _ in range(1000)]
        result = self.sorter.sort(data)
        self.assertEqual(result, sorted(data))
        stats = self.sorter.get_stats()
        self.assertLess(stats["execution_time"], 1.0)
    
    def test_performance_nearly_sorted_1000(self):
        data = list(range(1000))
        for i in range(0, 1000, 100):
            if i + 1 < 1000:
                data[i], data[i + 1] = data[i + 1], data[i]
        
        result = self.sorter.sort(data)
        self.assertEqual(result, sorted(data))
        stats = self.sorter.get_stats()
        self.assertLess(stats["execution_time"], 0.5)
    
    def test_performance_reverse_1000(self):
        data = list(range(1000, 0, -1))
        result = self.sorter.sort(data)
        self.assertEqual(result, sorted(data))
        stats = self.sorter.get_stats()
        self.assertLess(stats["execution_time"], 1.0)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestInputCharacteristics))
    suite.addTests(loader.loadTestsFromTestCase(TestSmartSort))
    suite.addTests(loader.loadTestsFromTestCase(TestAdaptiveStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    run_tests()
