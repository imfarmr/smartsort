import random
import time
from typing import List, Dict, Tuple
from smart_sort import SmartSort, InputCharacteristics


class SmartSortVisualizer:
    
    def __init__(self):
        self.bar_width = 50
    
    def create_bar_chart(self, value: int, max_value: int, width: int = 50) -> str:
        if max_value == 0:
            return ""
        
        filled = int((value / max_value) * width)
        bar = "█" * filled + "░" * (width - filled)
        return bar
    
    def visualize_array(self, data: List[int], title: str = "Array"):
        if not data:
            print(f"{title}: []")
            return
        
        max_val = max(data)
        min_val = min(data)
        
        print(f"\n{title}:")
        print(f"Size: {len(data)}, Range: [{min_val}, {max_val}]")
        
        if len(data) <= 20:
            print("Values:", data)
            print("\nVisualization:")
            for i, val in enumerate(data):
                bar = self.create_bar_chart(val - min_val, max_val - min_val, 30)
                print(f"  [{i:2d}] {val:5d} {bar}")
        else:
            print(f"First 10: {data[:10]}")
            print(f"Last 10:  {data[-10:]}")
    
    def visualize_characteristics(self, chars: InputCharacteristics):
        print("\n" + "="*60)
        print("INPUT CHARACTERISTICS ANALYSIS")
        print("="*60)
        
        print(f"\nSize: {chars.size}")
        print(f"Range: {chars.data_range[0]} to {chars.data_range[1]}")
        print(f"Has Duplicates: {chars.has_duplicates}")
        print(f"Distribution Type: {chars.distribution_type}")
        
        print(f"\nPresortedness: {chars.presortedness:.2%}")
        presorted_bar = self.create_bar_chart(int(chars.presortedness * 100), 100, 40)
        print(f"  {presorted_bar} {chars.presortedness:.2%}")
        
        print(f"\nRange Density: {chars.range_density:.2%}")
        density_bar = self.create_bar_chart(int(chars.range_density * 100), 100, 40)
        print(f"  {density_bar} {chars.range_density:.2%}")
        
        print("\nInterpretation:")
        if chars.presortedness >= 0.7:
            print("  ✓ High presortedness - InsertionSort recommended")
        elif chars.presortedness <= 0.3:
            print("  ✗ Low presortedness - Avoid InsertionSort")
        else:
            print("  ~ Medium presortedness")
        
        if chars.range_density >= 0.01 and chars.data_range[0] >= 0:
            print("  ✓ Dense range - RadixSort candidate")
        else:
            print("  ✗ Sparse range - RadixSort not optimal")
    
    def visualize_sorting_process(self, data: List[int], title: str = "Sorting Process"):
        print("\n" + "="*60)
        print(f"{title}")
        print("="*60)
        
        self.visualize_array(data, "Original Array")
        
        chars = InputCharacteristics(data)
        self.visualize_characteristics(chars)
        
        print("\n" + "="*60)
        print("EXECUTING SMARTSORT")
        print("="*60)
        
        sorter = SmartSort(verbose=False)
        start_time = time.perf_counter()
        sorted_data = sorter.sort(data)
        end_time = time.perf_counter()
        
        self.visualize_array(sorted_data, "Sorted Array")
        
        print("\n" + "="*60)
        print("SORTING STATISTICS")
        print("="*60)
        
        stats = sorter.get_stats()
        
        print(f"\nExecution Time: {stats['execution_time']*1000:.4f} ms")
        print(f"Comparisons: {stats['comparisons']:,}")
        print(f"Swaps: {stats['swaps']:,}")
        
        print("\nStrategy Usage:")
        strategy_counts = {}
        total_elements = 0
        
        for switch in stats['strategy_switches']:
            strategy = switch['strategy']
            size = switch['size']
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            total_elements += size
        
        for strategy, count in sorted(strategy_counts.items()):
            percentage = (count / len(stats['strategy_switches'])) * 100
            bar = self.create_bar_chart(int(percentage), 100, 30)
            print(f"  {strategy:15s}: {count:2d}x {bar} {percentage:.1f}%")
        
        print("\nStrategy Timeline:")
        for i, switch in enumerate(stats['strategy_switches'][:10]):
            print(f"  {i+1}. {switch['strategy']:15s} - Range [{switch['range'][0]:4d}:{switch['range'][1]:4d}] (size: {switch['size']:4d})")
        
        if len(stats['strategy_switches']) > 10:
            print(f"  ... and {len(stats['strategy_switches']) - 10} more strategy switches")
        
        is_correct = sorted_data == sorted(data)
        print(f"\nCorrectness Check: {'✓ PASSED' if is_correct else '✗ FAILED'}")
        
        return sorted_data, stats
    
    def compare_strategies(self, data: List[int]):
        print("\n" + "="*60)
        print("STRATEGY COMPARISON")
        print("="*60)
        
        print(f"\nTesting with {len(data)} elements")
        
        sorter = SmartSort(verbose=False)
        
        print("\n1. SmartSort (Adaptive):")
        start = time.perf_counter()
        result1 = sorter.sort(data)
        time1 = time.perf_counter() - start
        stats1 = sorter.get_stats()
        
        strategies_used = set(s['strategy'] for s in stats1['strategy_switches'])
        print(f"   Time: {time1*1000:.4f} ms")
        print(f"   Strategies: {', '.join(strategies_used)}")
        print(f"   Comparisons: {stats1['comparisons']:,}")
        
        print("\n2. Python Built-in sorted():")
        start = time.perf_counter()
        result2 = sorted(data)
        time2 = time.perf_counter() - start
        print(f"   Time: {time2*1000:.4f} ms")
        
        print("\n3. Python list.sort():")
        data_copy = data.copy()
        start = time.perf_counter()
        data_copy.sort()
        time3 = time.perf_counter() - start
        print(f"   Time: {time3*1000:.4f} ms")
        
        print("\nSpeed Comparison:")
        fastest_time = min(time1, time2, time3)
        print(f"  SmartSort:     {time1/fastest_time:6.2f}x {'(fastest)' if time1 == fastest_time else ''}")
        print(f"  sorted():      {time2/fastest_time:6.2f}x {'(fastest)' if time2 == fastest_time else ''}")
        print(f"  list.sort():   {time3/fastest_time:6.2f}x {'(fastest)' if time3 == fastest_time else ''}")
    
    def interactive_demo(self):
        print("\n" + "="*60)
        print("SMARTSORT INTERACTIVE VISUALIZATION")
        print("="*60)
        
        demos = [
            {
                "name": "Nearly Sorted Array",
                "data": [1, 2, 3, 4, 5, 7, 6, 8, 9, 10, 11, 12, 13, 15, 14, 16, 17, 18, 19, 20],
                "description": "Array with just a few elements out of place"
            },
            {
                "name": "Reverse Sorted Array",
                "data": [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                "description": "Completely reversed array"
            },
            {
                "name": "Dense Integer Range",
                "data": [5, 2, 8, 1, 9, 3, 7, 4, 6, 0, 5, 2, 8, 1, 9, 3, 7, 4, 6, 0] * 3,
                "description": "Small range of integers repeated multiple times"
            },
            {
                "name": "Random Array",
                "data": [random.randint(1, 100) for _ in range(50)],
                "description": "Randomly generated integers"
            },
            {
                "name": "Mountain Pattern",
                "data": list(range(1, 11)) + list(range(10, 0, -1)),
                "description": "Values increase then decrease"
            },
            {
                "name": "Sparse Large Range",
                "data": [1000, 50, 5000, 200, 10000, 300, 15000, 400],
                "description": "Large gaps between values"
            }
        ]
        
        for i, demo in enumerate(demos, 1):
            print(f"\n{'='*60}")
            print(f"DEMO {i}/{len(demos)}: {demo['name']}")
            print(f"{'='*60}")
            print(f"Description: {demo['description']}")
            
            self.visualize_sorting_process(demo['data'], demo['name'])
            
            if i < len(demos):
                print("\n" + "-"*60)
                input("Press Enter to continue to next demo...")


def demonstrate_adaptive_behavior():
    visualizer = SmartSortVisualizer()
    
    print("\n" + "="*60)
    print("DEMONSTRATING ADAPTIVE BEHAVIOR")
    print("="*60)
    
    test_cases = [
        ("Small Array (5 elements)", [5, 2, 8, 1, 9]),
        ("Medium Nearly Sorted (30 elements)", list(range(30)) + [28]),
        ("Large Random (100 elements)", [random.randint(1, 1000) for _ in range(100)]),
    ]
    
    for name, data in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {name}")
        print(f"{'='*60}")
        
        chars = InputCharacteristics(data)
        print(f"\nSize: {chars.size}")
        print(f"Presortedness: {chars.presortedness:.2%}")
        print(f"Range Density: {chars.range_density:.2%}")
        
        sorter = SmartSort(verbose=False)
        sorter.sort(data)
        stats = sorter.get_stats()
        
        strategies = {}
        for switch in stats['strategy_switches']:
            strategy = switch['strategy']
            strategies[strategy] = strategies.get(strategy, 0) + 1
        
        print(f"\nStrategies Selected:")
        for strategy, count in strategies.items():
            print(f"  - {strategy}: {count} time(s)")
        
        print(f"\nPerformance:")
        print(f"  Time: {stats['execution_time']*1000:.4f} ms")
        print(f"  Comparisons: {stats['comparisons']:,}")
        print(f"  Swaps: {stats['swaps']:,}")


def main():
    visualizer = SmartSortVisualizer()
    
    print("\n" + "="*70)
    print(" "*15 + "SMARTSORT VISUALIZATION SUITE")
    print("="*70)
    
    print("\nThis tool provides visual insights into SmartSort's adaptive behavior.")
    print("\nOptions:")
    print("  1. Interactive Demo (6 different scenarios)")
    print("  2. Adaptive Behavior Analysis")
    print("  3. Strategy Comparison")
    print("  4. Custom Array Visualization")
    
    choice = input("\nSelect option (1-4, or Enter for full demo): ").strip()
    
    if choice == "1":
        visualizer.interactive_demo()
    elif choice == "2":
        demonstrate_adaptive_behavior()
    elif choice == "3":
        print("\nGenerating test data...")
        data = [random.randint(1, 1000) for _ in range(100)]
        visualizer.compare_strategies(data)
    elif choice == "4":
        print("\nEnter array elements (space-separated integers):")
        try:
            data = list(map(int, input().split()))
            visualizer.visualize_sorting_process(data, "Custom Array")
        except ValueError:
            print("Invalid input. Using default array.")
            data = [64, 34, 25, 12, 22, 11, 90]
            visualizer.visualize_sorting_process(data, "Default Array")
    else:
        print("\nRunning full demonstration...")
        visualizer.interactive_demo()


if __name__ == "__main__":
    main()
