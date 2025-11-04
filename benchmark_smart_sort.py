import time
import random
import statistics
from typing import List, Callable, Dict, Tuple
from smart_sort import SmartSort


class SortingBenchmark:
    
    def __init__(self):
        self.results = []
    
    def generate_test_data(self, size: int, data_type: str) -> List[int]:
        random.seed(42)
        
        if data_type == "random":
            return [random.randint(1, size * 10) for _ in range(size)]
        
        elif data_type == "sorted":
            return list(range(size))
        
        elif data_type == "reverse":
            return list(range(size, 0, -1))
        
        elif data_type == "nearly_sorted":
            data = list(range(size))
            swaps = max(1, size // 20)
            for _ in range(swaps):
                i, j = random.randint(0, size-1), random.randint(0, size-1)
                data[i], data[j] = data[j], data[i]
            return data
        
        elif data_type == "few_unique":
            return [random.randint(1, 10) for _ in range(size)]
        
        elif data_type == "dense_range":
            return [random.randint(0, size // 10) for _ in range(size)]
        
        elif data_type == "sparse_range":
            return [random.randint(1, size * 100) for _ in range(size)]
        
        elif data_type == "alternating":
            return [i if i % 2 == 0 else size - i for i in range(size)]
        
        else:
            return [random.randint(1, size) for _ in range(size)]
    
    def benchmark_algorithm(self, sort_func: Callable, data: List[int], 
                          name: str, runs: int = 5) -> Dict:
        times = []
        comparisons_list = []
        swaps_list = []
        
        for _ in range(runs):
            data_copy = data.copy()
            
            if isinstance(sort_func, SmartSort):
                start = time.perf_counter()
                result = sort_func.sort(data_copy)
                end = time.perf_counter()
                
                stats = sort_func.get_stats()
                comparisons_list.append(stats["comparisons"])
                swaps_list.append(stats["swaps"])
            else:
                start = time.perf_counter()
                result = sort_func(data_copy)
                end = time.perf_counter()
            
            times.append(end - start)
            
            if result != sorted(data):
                raise ValueError(f"{name} produced incorrect result!")
        
        return {
            "name": name,
            "avg_time": statistics.mean(times),
            "min_time": min(times),
            "max_time": max(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "avg_comparisons": statistics.mean(comparisons_list) if comparisons_list else None,
            "avg_swaps": statistics.mean(swaps_list) if swaps_list else None
        }
    
    def python_builtin_sort(self, data: List[int]) -> List[int]:
        return sorted(data)
    
    def python_list_sort(self, data: List[int]) -> List[int]:
        data.sort()
        return data
    
    def run_comparison_benchmark(self, size: int, data_type: str, runs: int = 5):
        print(f"\n{'='*70}")
        print(f"Benchmark: {data_type.upper()} data, Size: {size}, Runs: {runs}")
        print(f"{'='*70}")
        
        data = self.generate_test_data(size, data_type)
        
        algorithms = [
            (SmartSort(verbose=False), "SmartSort (Adaptive)"),
            (self.python_builtin_sort, "Python sorted()"),
            (self.python_list_sort, "Python list.sort()")
        ]
        
        results = []
        for algo, name in algorithms:
            try:
                result = self.benchmark_algorithm(algo, data, name, runs)
                results.append(result)
                
                print(f"\n{name}:")
                print(f"  Average Time: {result['avg_time']*1000:.4f} ms")
                print(f"  Min Time:     {result['min_time']*1000:.4f} ms")
                print(f"  Max Time:     {result['max_time']*1000:.4f} ms")
                print(f"  Std Dev:      {result['std_dev']*1000:.4f} ms")
                
                if result['avg_comparisons'] is not None:
                    print(f"  Avg Comparisons: {result['avg_comparisons']:.0f}")
                    print(f"  Avg Swaps:       {result['avg_swaps']:.0f}")
            
            except Exception as e:
                print(f"\n{name}: ERROR - {str(e)}")
        
        if len(results) > 1:
            fastest = min(results, key=lambda x: x['avg_time'])
            print(f"\n{'='*70}")
            print(f"Fastest: {fastest['name']} ({fastest['avg_time']*1000:.4f} ms)")
            print(f"{'='*70}")
        
        return results
    
    def run_comprehensive_benchmark(self):
        print("\n" + "="*70)
        print("COMPREHENSIVE SMARTSORT BENCHMARK")
        print("="*70)
        
        test_configs = [
            (100, "random"),
            (100, "sorted"),
            (100, "reverse"),
            (100, "nearly_sorted"),
            (100, "dense_range"),
            (500, "random"),
            (500, "nearly_sorted"),
            (500, "few_unique"),
            (1000, "random"),
            (1000, "sorted"),
            (1000, "reverse"),
            (1000, "sparse_range"),
        ]
        
        all_results = []
        for size, data_type in test_configs:
            results = self.run_comparison_benchmark(size, data_type, runs=3)
            all_results.append({
                "size": size,
                "type": data_type,
                "results": results
            })
        
        self._print_summary(all_results)
    
    def _print_summary(self, all_results: List[Dict]):
        print("\n" + "="*70)
        print("BENCHMARK SUMMARY")
        print("="*70)
        
        smart_sort_wins = 0
        total_tests = len(all_results)
        
        for test in all_results:
            size = test["size"]
            data_type = test["type"]
            results = test["results"]
            
            if len(results) > 0:
                smart_sort_result = next((r for r in results if "SmartSort" in r["name"]), None)
                fastest = min(results, key=lambda x: x['avg_time'])
                
                if smart_sort_result and smart_sort_result["name"] == fastest["name"]:
                    smart_sort_wins += 1
                    winner = "SmartSort"
                else:
                    winner = fastest["name"]
                
                print(f"\n{data_type:15s} (n={size:4d}): Winner = {winner}")
        
        print(f"\n{'='*70}")
        print(f"SmartSort won {smart_sort_wins}/{total_tests} tests")
        print(f"Win rate: {(smart_sort_wins/total_tests)*100:.1f}%")
        print(f"{'='*70}")
    
    def analyze_strategy_selection(self):
        print("\n" + "="*70)
        print("STRATEGY SELECTION ANALYSIS")
        print("="*70)
        
        test_cases = [
            ("Small Array", [5, 2, 8, 1, 9, 3, 7]),
            ("Nearly Sorted", [1, 2, 3, 4, 5, 7, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]),
            ("Dense Range", [5, 2, 8, 1, 9, 3, 7, 4, 6, 0] * 5),
            ("Random Large", [random.randint(1, 10000) for _ in range(100)]),
            ("Sparse Range", [random.randint(1, 100000) for _ in range(50)]),
            ("Reverse Sorted", list(range(100, 0, -1)))
        ]
        
        for name, data in test_cases:
            sorter = SmartSort(verbose=False)
            sorter.sort(data)
            stats = sorter.get_stats()
            
            print(f"\n{name}:")
            print(f"  Size: {len(data)}")
            
            strategy_counts = {}
            for switch in stats["strategy_switches"]:
                strategy = switch["strategy"]
                strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            
            print(f"  Strategies Used:")
            for strategy, count in strategy_counts.items():
                print(f"    - {strategy}: {count} time(s)")
            
            print(f"  Comparisons: {stats['comparisons']}")
            print(f"  Swaps: {stats['swaps']}")
            print(f"  Time: {stats['execution_time']*1000:.4f} ms")


def main():
    benchmark = SortingBenchmark()
    
    print("\n" + "="*70)
    print("SmartSort Benchmarking Suite")
    print("="*70)
    
    print("\n1. Strategy Selection Analysis")
    benchmark.analyze_strategy_selection()
    
    print("\n\n2. Performance Comparison")
    benchmark.run_comprehensive_benchmark()


if __name__ == "__main__":
    main()
