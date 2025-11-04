# SmartSort - Adaptive Sorting Algorithm

An intelligent sorting algorithm that dynamically adapts to input characteristics and switches between different sorting strategies mid-execution for optimal performance.

## Features

### Adaptive Strategy Selection
SmartSort analyzes input data and automatically selects the most efficient sorting algorithm based on:

- **Presortedness**: Measures how close the data is to being sorted
- **Range Density**: Analyzes the distribution of values relative to their range
- **Data Distribution**: Identifies patterns (uniform, normal, skewed)
- **Size**: Considers array size for algorithm selection
- **Duplicate Detection**: Identifies presence of duplicate values

### Supported Sorting Algorithms

1. **Insertion Sort**
   - Used for: Small arrays (≤20 elements), nearly sorted data (≥70% presorted)
   - Time Complexity: O(n²) worst case, O(n) best case
   - Space Complexity: O(1)

2. **Merge Sort**
   - Used for: Large random arrays, general-purpose sorting
   - Time Complexity: O(n log n) guaranteed
   - Space Complexity: O(n)

3. **Radix Sort**
   - Used for: Dense integer ranges with good range density
   - Time Complexity: O(d·n) where d is number of digits
   - Space Complexity: O(n + k)

### Dynamic Adaptation

SmartSort doesn't just pick one algorithm at the start. It:
- Continuously analyzes subsections of data during recursive operations
- Switches strategies mid-execution when beneficial
- Tracks all strategy switches for performance analysis
- Optimizes for both time and space complexity

## Installation

No external dependencies required. Uses only Python standard library.

```bash
python smart_sort.py
```

## Usage

### Basic Usage

```python
from smart_sort import SmartSort

data = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
sorter = SmartSort()
sorted_data = sorter.sort(data)
print(sorted_data)
```

### Verbose Mode

```python
sorter = SmartSort(verbose=True)
sorted_data = sorter.sort(data)
```

### Accessing Statistics

```python
sorter = SmartSort()
sorted_data = sorter.sort(data)
stats = sorter.get_stats()

print(f"Comparisons: {stats['comparisons']}")
print(f"Swaps: {stats['swaps']}")
print(f"Execution Time: {stats['execution_time']}")
print(f"Strategies Used: {stats['strategy_switches']}")
```

## Architecture

### InputCharacteristics Class

Analyzes input data to determine optimal sorting strategy:

```python
characteristics = InputCharacteristics(data)
print(characteristics.presortedness)      # 0.0 to 1.0
print(characteristics.range_density)      # 0.0 to 1.0
print(characteristics.distribution_type)  # 'normal', 'skewed', etc.
print(characteristics.has_duplicates)     # True/False
```

### SmartSort Class

Main sorting engine with adaptive capabilities:

- `sort(data)`: Main sorting method
- `get_stats()`: Returns performance statistics
- `_select_strategy()`: Chooses optimal algorithm
- `_adaptive_sort()`: Recursive sorting with strategy switching

## Algorithm Selection Logic

```
IF size ≤ 20:
    USE InsertionSort
ELSE IF presortedness ≥ 0.7:
    USE InsertionSort
ELSE IF range_density ≥ 0.01 AND range < size×10 AND all_positive:
    USE RadixSort
ELSE:
    USE MergeSort
```

## Performance Characteristics

### Best Cases
- **Nearly Sorted Data**: O(n) with InsertionSort
- **Dense Integer Range**: O(d·n) with RadixSort
- **Small Arrays**: O(n²) but with low constant factors

### Worst Cases
- **Random Large Arrays**: O(n log n) with MergeSort
- **Sparse Integer Range**: O(n log n) with MergeSort

### Space Complexity
- O(1) for InsertionSort segments
- O(n) for MergeSort segments
- O(n + k) for RadixSort segments

## Testing

Run the comprehensive test suite:

```bash
python test_smart_sort.py
```

Test coverage includes:
- Input characteristics analysis
- Correctness verification
- Strategy selection validation
- Edge cases
- Performance benchmarks

## Benchmarking

Compare SmartSort against Python's built-in sorting:

```bash
python benchmark_smart_sort.py
```

Benchmark features:
- Multiple data types (random, sorted, reverse, nearly sorted, etc.)
- Various array sizes (100, 500, 1000+ elements)
- Strategy selection analysis
- Performance comparison with Python's Timsort
- Statistical analysis (mean, min, max, std dev)

## Examples

### Example 1: Nearly Sorted Array
```python
data = [1, 2, 3, 5, 4, 6, 7, 8, 9, 10]
sorter = SmartSort(verbose=True)
result = sorter.sort(data)
```
**Strategy**: InsertionSort (high presortedness detected)

### Example 2: Dense Range
```python
data = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0] * 10
sorter = SmartSort(verbose=True)
result = sorter.sort(data)
```
**Strategy**: RadixSort (dense integer range detected)

### Example 3: Random Large Array
```python
import random
data = [random.randint(1, 10000) for _ in range(1000)]
sorter = SmartSort(verbose=True)
result = sorter.sort(data)
```
**Strategy**: MergeSort with InsertionSort for small segments

## Statistics Tracking

SmartSort tracks detailed performance metrics:

```python
stats = {
    "comparisons": 1234,
    "swaps": 567,
    "execution_time": 0.001234,
    "strategy_switches": [
        {"strategy": "MergeSort", "range": (0, 100), "size": 100},
        {"strategy": "InsertionSort", "range": (0, 15), "size": 15}
    ]
}
```

## Advantages

1. **Adaptive**: Automatically selects optimal algorithm
2. **Efficient**: Exploits data characteristics for better performance
3. **Transparent**: Provides detailed statistics and strategy information
4. **Robust**: Handles edge cases and various data patterns
5. **Educational**: Clear implementation for learning algorithm design

## Limitations

1. **Integer-only RadixSort**: Current RadixSort implementation only handles non-negative integers
2. **Overhead**: Analysis adds small overhead for very small arrays
3. **Memory**: MergeSort segments require O(n) additional space

## Future Enhancements

- Support for custom comparison functions
- Parallel sorting for large datasets
- Additional algorithms (HeapSort, QuickSort with pivot selection)
- Floating-point RadixSort support
- Adaptive threshold tuning based on hardware

## License

Open source - feel free to use and modify.

## Contributing

Contributions welcome! Areas for improvement:
- Additional sorting algorithms
- Better heuristics for strategy selection
- Performance optimizations
- Extended test coverage
