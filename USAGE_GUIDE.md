# SmartSort Usage Guide

## Quick Start

### Basic Sorting

```python
from smart_sort import SmartSort

data = [64, 34, 25, 12, 22, 11, 90]
sorter = SmartSort()
sorted_data = sorter.sort(data)
print(sorted_data)
```

### Verbose Mode for Debugging

```python
sorter = SmartSort(verbose=True)
sorted_data = sorter.sort(data)
```

Output shows:
- Input characteristics analysis
- Strategy selection decisions
- Performance statistics

## Running the Examples

### 1. Basic Demonstration
```bash
python smart_sort.py
```
Shows 6 different test cases with various data patterns.

### 2. Run All Tests
```bash
python test_smart_sort.py
```
Executes 32 comprehensive unit tests.

### 3. Performance Benchmarking
```bash
python benchmark_smart_sort.py
```
Compares SmartSort with Python's built-in sorting across multiple scenarios.

### 4. Visual Analysis
```bash
python visualize_smart_sort.py
```
Interactive visualization tool with multiple demo scenarios.

### 5. Advanced Examples
```bash
python advanced_examples.py
```
Real-world use case demonstrations.

## Understanding the Output

### Input Characteristics

```
InputCharacteristics(
    size=15,
    presortedness=0.98,      # 98% sorted
    range_density=1.00,      # Dense range
    distribution=normal,
    duplicates=False
)
```

**Presortedness**: 
- 1.0 = Fully sorted
- 0.0 = Reverse sorted
- 0.7+ = Nearly sorted (triggers InsertionSort)

**Range Density**:
- 1.0 = All consecutive values
- 0.01+ = Dense enough for RadixSort
- <0.01 = Sparse (use MergeSort)

### Strategy Selection

SmartSort automatically chooses:

1. **InsertionSort** when:
   - Array size ≤ 20 elements
   - Presortedness ≥ 70%

2. **RadixSort** when:
   - Range density ≥ 1%
   - Value range < size × 10
   - All values are non-negative

3. **MergeSort** for:
   - Large random arrays
   - Sparse value ranges
   - General-purpose sorting

### Statistics Output

```python
stats = sorter.get_stats()

{
    "comparisons": 1234,
    "swaps": 567,
    "execution_time": 0.001234,
    "strategy_switches": [
        {
            "strategy": "MergeSort",
            "range": (0, 100),
            "size": 100
        }
    ]
}
```

## Common Use Cases

### Case 1: Sorting Nearly Sorted Data

```python
data = list(range(1000))
data[500], data[501] = data[501], data[500]

sorter = SmartSort(verbose=True)
result = sorter.sort(data)
```

**Expected**: InsertionSort selected, O(n) performance

### Case 2: Sorting Age Data

```python
import random
ages = [random.randint(0, 120) for _ in range(1000)]

sorter = SmartSort()
sorted_ages = sorter.sort(ages)
```

**Expected**: RadixSort selected for dense integer range

### Case 3: Random Data

```python
import random
data = [random.randint(1, 100000) for _ in range(1000)]

sorter = SmartSort()
result = sorter.sort(data)
```

**Expected**: MergeSort with InsertionSort for small segments

### Case 4: Small Arrays

```python
data = [5, 2, 8, 1, 9]
sorter = SmartSort()
result = sorter.sort(data)
```

**Expected**: InsertionSort (optimal for small arrays)

## Analyzing Your Data

### Check Input Characteristics

```python
from smart_sort import InputCharacteristics

data = [your_data_here]
chars = InputCharacteristics(data)

print(f"Size: {chars.size}")
print(f"Presortedness: {chars.presortedness:.2%}")
print(f"Range Density: {chars.range_density:.2%}")
print(f"Distribution: {chars.distribution_type}")
print(f"Has Duplicates: {chars.has_duplicates}")
print(f"Range: {chars.data_range}")
```

This helps you understand what strategy SmartSort will choose.

## Performance Tips

### When SmartSort Excels

1. **Nearly Sorted Data**: Up to O(n) performance
2. **Dense Integer Ranges**: Efficient RadixSort usage
3. **Mixed Patterns**: Adapts to local characteristics

### When to Use Python's Built-in Sort

1. **Production Code**: Python's Timsort is highly optimized in C
2. **Custom Comparisons**: Built-in sort supports key functions
3. **Stability Required**: Timsort is stable by design

### SmartSort Best For

1. **Educational Purposes**: Understanding adaptive algorithms
2. **Algorithm Research**: Experimenting with strategy selection
3. **Transparent Analysis**: Detailed statistics and insights

## Customization

### Adjusting Thresholds

Modify these constants in `SmartSort` class:

```python
class SmartSort:
    INSERTION_THRESHOLD = 20        # Max size for InsertionSort
    RADIX_DENSITY_THRESHOLD = 0.01  # Min density for RadixSort
    PRESORTED_THRESHOLD = 0.7       # Min presortedness for InsertionSort
```

### Adding Custom Strategies

1. Implement your sorting algorithm
2. Add detection logic in `_select_strategy()`
3. Call your algorithm in `_adaptive_sort()`

Example:

```python
def _quick_sort(self, data, left, right):
    # Your QuickSort implementation
    pass

def _select_strategy(self, characteristics):
    # Add your logic
    if some_condition:
        return SortStrategy.QUICK_SORT
    # ... existing logic
```

## Troubleshooting

### Issue: Negative Numbers Not Sorting

**Cause**: Current RadixSort only handles non-negative integers

**Solution**: SmartSort automatically falls back to MergeSort for negative numbers

### Issue: Slow Performance on Large Arrays

**Cause**: Python implementation vs C-optimized built-in sort

**Solution**: This is expected. SmartSort is educational, not production-optimized

### Issue: Unexpected Strategy Selection

**Solution**: Use verbose mode to see why:

```python
sorter = SmartSort(verbose=True)
result = sorter.sort(data)
```

## Testing Your Own Data

### Create a Test Script

```python
from smart_sort import SmartSort, InputCharacteristics

your_data = [...]  # Your data here

print("Analyzing your data...")
chars = InputCharacteristics(your_data)
print(chars)

print("\nSorting...")
sorter = SmartSort(verbose=True)
result = sorter.sort(your_data)

print("\nVerifying correctness...")
assert result == sorted(your_data), "Sort failed!"
print("✓ Correct!")

stats = sorter.get_stats()
print(f"\nTime: {stats['execution_time']*1000:.4f} ms")
print(f"Comparisons: {stats['comparisons']:,}")
```

## Visualization Options

### Option 1: Bar Charts (visualize_smart_sort.py)

Shows visual representation of:
- Array values as bars
- Presortedness and density metrics
- Strategy usage breakdown

### Option 2: Statistics Summary

```python
sorter = SmartSort(verbose=False)
result = sorter.sort(data)
stats = sorter.get_stats()

print(f"Execution Time: {stats['execution_time']*1000:.4f} ms")
print(f"Comparisons: {stats['comparisons']:,}")
print(f"Swaps: {stats['swaps']:,}")

for switch in stats['strategy_switches']:
    print(f"  {switch['strategy']} on range {switch['range']}")
```

## Integration Examples

### Sorting Custom Objects

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [Person("Alice", 30), Person("Bob", 25), ...]

ages = [p.age for p in people]
sorted_indices = sorted(range(len(ages)), key=lambda i: ages[i])

sorter = SmartSort()
sorted_ages = sorter.sort(ages)
```

### Batch Processing

```python
datasets = [
    [5, 2, 8, 1, 9],
    [64, 34, 25, 12, 22],
    list(range(100, 0, -1))
]

sorter = SmartSort()
results = [sorter.sort(data) for data in datasets]
```

## Further Reading

- **README_SMARTSORT.md**: Complete documentation
- **SMARTSORT_SUMMARY.md**: Implementation details
- **Source code**: Fully documented with inline explanations

## Support

For issues or questions:
1. Check verbose output for strategy decisions
2. Review input characteristics
3. Examine test cases for similar patterns
4. Modify thresholds if needed
