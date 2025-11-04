# SmartSort Quick Reference Card

## Installation & Setup
```bash
cd c:\Users\hp\Desktop\pailasim
python smart_sort.py
```

## Basic Usage

### Sort an Array
```python
from smart_sort import SmartSort

data = [64, 34, 25, 12, 22, 11, 90]
sorter = SmartSort()
result = sorter.sort(data)
```

### With Verbose Output
```python
sorter = SmartSort(verbose=True)
result = sorter.sort(data)
```

### Get Statistics
```python
stats = sorter.get_stats()
print(stats['execution_time'])
print(stats['comparisons'])
print(stats['swaps'])
```

## Analyze Data Characteristics

```python
from smart_sort import InputCharacteristics

chars = InputCharacteristics(data)
print(chars.presortedness)    # 0.0 to 1.0
print(chars.range_density)    # 0.0 to 1.0
print(chars.distribution_type)
```

## Strategy Selection Rules

| Condition | Strategy | Time Complexity |
|-----------|----------|-----------------|
| Size ≤ 20 | InsertionSort | O(n²) |
| Presorted ≥ 70% | InsertionSort | O(n) |
| Dense range + positive | RadixSort | O(d·n) |
| Default | MergeSort | O(n log n) |

## Command Reference

```bash
python smart_sort.py              # Run demo
python test_smart_sort.py         # Run tests (32 tests)
python benchmark_smart_sort.py    # Benchmark performance
python visualize_smart_sort.py    # Interactive visualization
python advanced_examples.py       # Real-world examples
```

## Key Metrics

### Presortedness
- **1.0**: Fully sorted
- **0.7+**: Nearly sorted (use InsertionSort)
- **0.5**: Random
- **0.0**: Reverse sorted

### Range Density
- **1.0**: Consecutive values
- **0.01+**: Dense (use RadixSort)
- **<0.01**: Sparse (use MergeSort)

## Common Patterns

### Nearly Sorted Data
```python
data = list(range(100))
data[50], data[51] = data[51], data[50]
```
**Expected**: InsertionSort, O(n)

### Dense Integer Range
```python
ages = [random.randint(0, 120) for _ in range(200)]
```
**Expected**: RadixSort, O(d·n)

### Random Large Array
```python
data = [random.randint(1, 10000) for _ in range(1000)]
```
**Expected**: MergeSort, O(n log n)

## Statistics Output

```python
{
    "comparisons": 1234,
    "swaps": 567,
    "execution_time": 0.001234,
    "strategy_switches": [
        {"strategy": "MergeSort", "range": (0, 100), "size": 100}
    ]
}
```

## Customization

### Adjust Thresholds
```python
SmartSort.INSERTION_THRESHOLD = 20
SmartSort.RADIX_DENSITY_THRESHOLD = 0.01
SmartSort.PRESORTED_THRESHOLD = 0.7
```

## File Overview

| File | Purpose |
|------|---------|
| smart_sort.py | Core algorithm |
| test_smart_sort.py | Unit tests |
| benchmark_smart_sort.py | Performance comparison |
| visualize_smart_sort.py | Visual analysis |
| advanced_examples.py | Use case examples |
| README_SMARTSORT.md | Full documentation |
| USAGE_GUIDE.md | User guide |
| PROJECT_OVERVIEW.md | Complete overview |

## Troubleshooting

### Slow Performance
**Cause**: Python implementation vs C-optimized built-in
**Solution**: Expected behavior, use for education not production

### Unexpected Strategy
**Solution**: Use `verbose=True` to see decision process

### Negative Numbers
**Note**: RadixSort skipped for negative numbers (uses MergeSort)

## Test Results
```
✓ 32/32 tests passed
✓ All sorting algorithms correct
✓ Strategy selection validated
✓ Edge cases handled
✓ Performance benchmarked
```

## Performance Summary

| Data Type | Size | Strategy | Time |
|-----------|------|----------|------|
| Nearly Sorted | 100 | InsertionSort | ~2ms |
| Dense Range | 200 | RadixSort | ~8ms |
| Random | 500 | MergeSort | ~48ms |
| Large Random | 1000 | MergeSort | ~165ms |

## Key Features

- ✓ Adaptive strategy selection
- ✓ Mid-execution switching
- ✓ Detailed statistics
- ✓ Three sorting algorithms
- ✓ Comprehensive testing
- ✓ Visual analysis tools

## Quick Commands

```bash
python smart_sort.py                    # Demo
python test_smart_sort.py               # Test
python benchmark_smart_sort.py          # Benchmark
python visualize_smart_sort.py          # Visualize
python advanced_examples.py             # Examples
```

---

**For detailed information, see:**
- README_SMARTSORT.md
- USAGE_GUIDE.md
- PROJECT_OVERVIEW.md
