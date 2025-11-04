import random
import time
from smart_sort import SmartSort, InputCharacteristics


def example_nearly_sorted():
    print("\n" + "="*70)
    print("EXAMPLE 1: Nearly Sorted Data Optimization")
    print("="*70)
    
    data = list(range(1, 101))
    for _ in range(5):
        i, j = random.randint(0, 99), random.randint(0, 99)
        data[i], data[j] = data[j], data[i]
    
    print(f"Data size: {len(data)}")
    chars = InputCharacteristics(data)
    print(f"Presortedness: {chars.presortedness:.2%}")
    
    sorter = SmartSort(verbose=False)
    result = sorter.sort(data)
    stats = sorter.get_stats()
    
    print(f"Strategy: InsertionSort (O(n) for nearly sorted)")
    print(f"Comparisons: {stats['comparisons']:,}")
    print(f"Time: {stats['execution_time']*1000:.4f} ms")


def example_dense_range():
    print("\n" + "="*70)
    print("EXAMPLE 2: Dense Integer Range")
    print("="*70)
    
    ages = [random.randint(0, 120) for _ in range(200)]
    
    chars = InputCharacteristics(ages)
    print(f"Range: {chars.data_range[0]} to {chars.data_range[1]}")
    print(f"Range Density: {chars.range_density:.2%}")
    
    sorter = SmartSort(verbose=False)
    result = sorter.sort(ages)
    stats = sorter.get_stats()
    
    strategies = set(s['strategy'] for s in stats['strategy_switches'])
    print(f"Strategies: {', '.join(strategies)}")
    print(f"Time: {stats['execution_time']*1000:.4f} ms")


def example_large_random():
    print("\n" + "="*70)
    print("EXAMPLE 3: Large Random Array")
    print("="*70)
    
    data = [random.randint(1, 10000) for _ in range(500)]
    
    sorter = SmartSort(verbose=False)
    result = sorter.sort(data)
    stats = sorter.get_stats()
    
    print(f"Data size: {len(data)}")
    print(f"Strategy: MergeSort with InsertionSort for small segments")
    print(f"Comparisons: {stats['comparisons']:,}")
    print(f"Time: {stats['execution_time']*1000:.4f} ms")


if __name__ == "__main__":
    print("SmartSort Advanced Examples")
    example_nearly_sorted()
    example_dense_range()
    example_large_random()
