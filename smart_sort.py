import time
import math
from typing import List, Tuple, Dict, Any
from enum import Enum


class SortStrategy(Enum):
    INSERTION_SORT = "InsertionSort"
    MERGE_SORT = "MergeSort"
    RADIX_SORT = "RadixSort"
    QUICK_SORT = "QuickSort"
    HYBRID = "Hybrid"


class InputCharacteristics:
    def __init__(self, data: List[int]):
        self.size = len(data)
        self.presortedness = self._calculate_presortedness(data)
        self.range_density = self._calculate_range_density(data)
        self.distribution_type = self._analyze_distribution(data)
        self.has_duplicates = self._check_duplicates(data)
        self.data_range = self._get_range(data)
        
    def _calculate_presortedness(self, data: List[int]) -> float:
        if len(data) <= 1:
            return 1.0
        
        runs = 0
        inversions = 0
        max_inversions = (len(data) * (len(data) - 1)) // 2
        
        for i in range(len(data) - 1):
            if data[i] <= data[i + 1]:
                runs += 1
            for j in range(i + 1, len(data)):
                if data[i] > data[j]:
                    inversions += 1
        
        if max_inversions == 0:
            return 1.0
        
        presorted_score = 1 - (inversions / max_inversions)
        return presorted_score
    
    def _calculate_range_density(self, data: List[int]) -> float:
        if len(data) == 0:
            return 0.0
        
        min_val = min(data)
        max_val = max(data)
        value_range = max_val - min_val
        
        if value_range == 0:
            return 1.0
        
        unique_count = len(set(data))
        density = unique_count / (value_range + 1)
        return density
    
    def _analyze_distribution(self, data: List[int]) -> str:
        if len(data) == 0:
            return "small"
        
        unique_values = len(set(data))
        if unique_values == 1:
            return "uniform"
        
        if len(data) < 10:
            return "small"
        
        sorted_data = sorted(data)
        q1 = sorted_data[len(data) // 4]
        q2 = sorted_data[len(data) // 2]
        q3 = sorted_data[3 * len(data) // 4]
        
        iqr = q3 - q1
        lower_spread = q2 - q1
        upper_spread = q3 - q2
        
        if iqr == 0:
            return "uniform"
        
        skew_ratio = abs(lower_spread - upper_spread) / iqr
        
        if skew_ratio < 0.2:
            return "normal"
        elif skew_ratio < 0.5:
            return "slightly_skewed"
        else:
            return "highly_skewed"
    
    def _check_duplicates(self, data: List[int]) -> bool:
        return len(data) != len(set(data))
    
    def _get_range(self, data: List[int]) -> Tuple[int, int]:
        if len(data) == 0:
            return (0, 0)
        return (min(data), max(data))
    
    def __repr__(self) -> str:
        return (f"InputCharacteristics(size={self.size}, "
                f"presortedness={self.presortedness:.2f}, "
                f"range_density={self.range_density:.2f}, "
                f"distribution={self.distribution_type}, "
                f"duplicates={self.has_duplicates})")


class SmartSort:
    INSERTION_THRESHOLD = 20
    RADIX_DENSITY_THRESHOLD = 0.01
    PRESORTED_THRESHOLD = 0.7
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stats = {
            "comparisons": 0,
            "swaps": 0,
            "strategy_switches": [],
            "execution_time": 0
        }
    
    def sort(self, data: List[int]) -> List[int]:
        start_time = time.time()
        self.stats = {
            "comparisons": 0,
            "swaps": 0,
            "strategy_switches": [],
            "execution_time": 0
        }
        
        if len(data) <= 1:
            return data.copy()
        
        result = data.copy()
        characteristics = InputCharacteristics(result)
        
        if self.verbose:
            print(f"\n{characteristics}")
        
        strategy = self._select_strategy(characteristics)
        self._log_strategy(strategy, 0, len(result))
        
        result = self._adaptive_sort(result, 0, len(result), characteristics)
        
        self.stats["execution_time"] = time.time() - start_time
        
        if self.verbose:
            self._print_stats()
        
        return result
    
    def _select_strategy(self, characteristics: InputCharacteristics) -> SortStrategy:
        if characteristics.size <= self.INSERTION_THRESHOLD:
            return SortStrategy.INSERTION_SORT
        
        if characteristics.presortedness >= self.PRESORTED_THRESHOLD:
            return SortStrategy.INSERTION_SORT
        
        min_val, max_val = characteristics.data_range
        value_range = max_val - min_val
        
        if (value_range > 0 and 
            characteristics.range_density >= self.RADIX_DENSITY_THRESHOLD and
            value_range < characteristics.size * 10 and
            min_val >= 0):
            return SortStrategy.RADIX_SORT
        
        return SortStrategy.MERGE_SORT
    
    def _adaptive_sort(self, data: List[int], left: int, right: int, 
                      characteristics: InputCharacteristics) -> List[int]:
        size = right - left
        
        if size <= 1:
            return data
        
        if size <= self.INSERTION_THRESHOLD:
            return self._insertion_sort(data, left, right)
        
        subset = data[left:right]
        local_chars = InputCharacteristics(subset)
        strategy = self._select_strategy(local_chars)
        
        if strategy == SortStrategy.INSERTION_SORT:
            return self._insertion_sort(data, left, right)
        elif strategy == SortStrategy.RADIX_SORT:
            sorted_subset = self._radix_sort(subset)
            data[left:right] = sorted_subset
            return data
        else:
            return self._merge_sort(data, left, right)
    
    def _insertion_sort(self, data: List[int], left: int, right: int) -> List[int]:
        for i in range(left + 1, right):
            key = data[i]
            j = i - 1
            while j >= left and data[j] > key:
                self.stats["comparisons"] += 1
                data[j + 1] = data[j]
                self.stats["swaps"] += 1
                j -= 1
            if j >= left:
                self.stats["comparisons"] += 1
            data[j + 1] = key
        return data
    
    def _merge_sort(self, data: List[int], left: int, right: int) -> List[int]:
        if right - left <= 1:
            return data
        
        if right - left <= self.INSERTION_THRESHOLD:
            return self._insertion_sort(data, left, right)
        
        mid = (left + right) // 2
        
        data = self._merge_sort(data, left, mid)
        data = self._merge_sort(data, mid, right)
        
        return self._merge(data, left, mid, right)
    
    def _merge(self, data: List[int], left: int, mid: int, right: int) -> List[int]:
        left_part = data[left:mid]
        right_part = data[mid:right]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            self.stats["comparisons"] += 1
            if left_part[i] <= right_part[j]:
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1
            self.stats["swaps"] += 1
            k += 1
        
        while i < len(left_part):
            data[k] = left_part[i]
            i += 1
            k += 1
            self.stats["swaps"] += 1
        
        while j < len(right_part):
            data[k] = right_part[j]
            j += 1
            k += 1
            self.stats["swaps"] += 1
        
        return data
    
    def _radix_sort(self, data: List[int]) -> List[int]:
        if not data:
            return data
        
        max_val = max(data)
        exp = 1
        
        while max_val // exp > 0:
            data = self._counting_sort_by_digit(data, exp)
            exp *= 10
        
        return data
    
    def _counting_sort_by_digit(self, data: List[int], exp: int) -> List[int]:
        n = len(data)
        output = [0] * n
        count = [0] * 10
        
        for i in range(n):
            index = (data[i] // exp) % 10
            count[index] += 1
            self.stats["comparisons"] += 1
        
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        for i in range(n - 1, -1, -1):
            index = (data[i] // exp) % 10
            output[count[index] - 1] = data[i]
            count[index] -= 1
            self.stats["swaps"] += 1
        
        return output
    
    def _log_strategy(self, strategy: SortStrategy, left: int, right: int):
        self.stats["strategy_switches"].append({
            "strategy": strategy.value,
            "range": (left, right),
            "size": right - left
        })
        
        if self.verbose:
            print(f"Using {strategy.value} for range [{left}:{right}] (size: {right - left})")
    
    def _print_stats(self):
        print("\n=== SmartSort Statistics ===")
        print(f"Execution Time: {self.stats['execution_time']:.6f} seconds")
        print(f"Comparisons: {self.stats['comparisons']}")
        print(f"Swaps: {self.stats['swaps']}")
        print(f"\nStrategy Usage:")
        
        strategy_counts = {}
        for switch in self.stats["strategy_switches"]:
            strategy = switch["strategy"]
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        for strategy, count in strategy_counts.items():
            print(f"  {strategy}: {count} time(s)")
    
    def get_stats(self) -> Dict[str, Any]:
        return self.stats.copy()


def demonstrate_smart_sort():
    print("=" * 60)
    print("SmartSort - Adaptive Sorting Algorithm Demonstration")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Nearly Sorted Array",
            "data": [1, 2, 3, 5, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14]
        },
        {
            "name": "Random Array",
            "data": [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 23, 36, 18, 77]
        },
        {
            "name": "Small Range Dense Array",
            "data": [5, 2, 8, 1, 9, 3, 7, 4, 6, 0, 5, 2, 8, 1, 9]
        },
        {
            "name": "Reverse Sorted",
            "data": [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5]
        },
        {
            "name": "Small Array",
            "data": [5, 2, 8, 1, 9]
        },
        {
            "name": "Large Range Sparse",
            "data": [1000, 50, 2000, 100, 3000, 150, 4000, 200]
        }
    ]
    
    for test in test_cases:
        print(f"\n{'=' * 60}")
        print(f"Test Case: {test['name']}")
        print(f"{'=' * 60}")
        print(f"Original: {test['data']}")
        
        sorter = SmartSort(verbose=True)
        sorted_data = sorter.sort(test['data'])
        
        print(f"Sorted:   {sorted_data}")
        print(f"Correct:  {sorted_data == sorted(test['data'])}")


if __name__ == "__main__":
    demonstrate_smart_sort()
