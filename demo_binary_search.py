"""
Binary Search Demonstration Script
Shows the performance difference between binary search and linear search
"""
import time
from pathlib import Path
from pcbuilder.database_manager import get_database_manager
from pcbuilder.search_algorithms import (
    binary_search_by_price,
    linear_search_by_price,
    binary_search_range,
    compare_search_algorithms
)
from pcbuilder.filters import find_component_by_price, find_components_in_price_range


def demo_search_comparison():
    """Demonstrate binary search vs linear search performance"""
    print("=" * 70)
    print("BINARY SEARCH ALGORITHM DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Load components from database
    db = get_database_manager()
    components = db.get_all_components()
    
    if not components:
        print("Error: No components found in database")
        return
    
    print(f"Loaded {len(components)} components from database")
    print()
    
    # Test 1: Find component closest to £250
    print("TEST 1: Find GPU closest to £250")
    print("-" * 70)
    
    gpus = [c for c in components if c.get_category() == "GPU"]
    print(f"Searching through {len(gpus)} GPUs...")
    print()
    
    # Linear search
    start = time.perf_counter()
    linear_result = linear_search_by_price(gpus, 250.0)
    linear_time = time.perf_counter() - start
    
    print(f"LINEAR SEARCH (O(n)):")
    print(f"  Result: {linear_result.name if linear_result else 'None'}")
    print(f"  Price: £{linear_result.price if linear_result else 0:.2f}")
    print(f"  Time: {linear_time * 1000:.4f} ms")
    print(f"  Comparisons: {len(gpus)} (worst case)")
    print()
    
    # Binary search (requires sorting)
    sorted_gpus = sorted(gpus, key=lambda c: c.price)
    start = time.perf_counter()
    binary_result = binary_search_by_price(sorted_gpus, 250.0)
    binary_time = time.perf_counter() - start
    
    print(f"BINARY SEARCH (O(log n)):")
    print(f"  Result: {binary_result.name if binary_result else 'None'}")
    print(f"  Price: £{binary_result.price if binary_result else 0:.2f}")
    print(f"  Time: {binary_time * 1000:.4f} ms")
    print(f"  Comparisons: ~{len(gpus).bit_length()} (log₂ n)")
    print()
    
    if binary_time > 0:
        speedup = linear_time / binary_time
        print(f"PERFORMANCE: Binary search is {speedup:.1f}x faster!")
    print()
    
    # Test 2: Find all components in price range
    print("TEST 2: Find all CPUs between £150 and £250")
    print("-" * 70)
    
    cpus = [c for c in components if c.get_category() == "CPU"]
    print(f"Searching through {len(cpus)} CPUs...")
    print()
    
    # Linear approach
    start = time.perf_counter()
    linear_range = [c for c in cpus if 150 <= c.price <= 250]
    linear_range_time = time.perf_counter() - start
    
    print(f"LINEAR FILTERING (O(n)):")
    print(f"  Found: {len(linear_range)} CPUs")
    print(f"  Time: {linear_range_time * 1000:.4f} ms")
    print()
    
    # Binary search approach
    sorted_cpus = sorted(cpus, key=lambda c: c.price)
    start = time.perf_counter()
    binary_range = binary_search_range(sorted_cpus, 150.0, 250.0)
    binary_range_time = time.perf_counter() - start
    
    print(f"BINARY SEARCH RANGE (O(log n + k)):")
    print(f"  Found: {len(binary_range)} CPUs")
    print(f"  Time: {binary_range_time * 1000:.4f} ms")
    print()
    
    if binary_range_time > 0:
        speedup = linear_range_time / binary_range_time
        print(f"PERFORMANCE: Binary search is {speedup:.1f}x faster!")
    print()
    
    # Show some results
    if binary_range:
        print("Sample results:")
        for cpu in binary_range[:5]:
            print(f"  • {cpu.name}: £{cpu.price:.2f}")
        if len(binary_range) > 5:
            print(f"  ... and {len(binary_range) - 5} more")
    print()
    
    # Test 3: Comprehensive comparison with all components
    print("TEST 3: Comprehensive Performance Analysis")
    print("-" * 70)
    
    comparison = compare_search_algorithms(components, 500.0)
    
    print(f"Dataset size: {comparison['list_size']} components")
    print(f"Target price: £{comparison['target_price']:.2f}")
    print()
    
    print("LINEAR SEARCH:")
    print(f"  Time: {comparison['linear_search']['time_seconds'] * 1000:.4f} ms")
    print(f"  Comparisons: {comparison['linear_search']['comparisons']}")
    print(f"  Result: {comparison['linear_search']['result']}")
    print()
    
    print("BINARY SEARCH:")
    print(f"  Search time: {comparison['binary_search']['time_seconds'] * 1000:.4f} ms")
    print(f"  Sort time: {comparison['binary_search']['sort_time_seconds'] * 1000:.4f} ms")
    print(f"  Total time: {comparison['binary_search']['total_time_seconds'] * 1000:.4f} ms")
    print(f"  Comparisons: ~{comparison['binary_search']['comparisons']}")
    print(f"  Result: {comparison['binary_search']['result']}")
    print()
    
    print(f"SPEEDUP: {comparison['speedup']:.2f}x")
    print()
    print(f"ANALYSIS: {comparison['analysis']}")
    print()
    
    # Test 4: Show algorithm complexity with different dataset sizes
    print("TEST 4: Algorithmic Complexity Demonstration")
    print("-" * 70)
    print()
    print("For n components:")
    print(f"  n = 10:    Linear = 10 ops,    Binary = ~{10 .bit_length()} ops")
    print(f"  n = 100:   Linear = 100 ops,   Binary = ~{100 .bit_length()} ops")
    print(f"  n = 187:   Linear = 187 ops,   Binary = ~{187 .bit_length()} ops")
    print(f"  n = 1000:  Linear = 1000 ops,  Binary = ~{1000 .bit_length()} ops")
    print(f"  n = 10000: Linear = 10000 ops, Binary = ~{10000 .bit_length()} ops")
    print()
    print("As dataset grows, binary search becomes exponentially more efficient!")
    print()
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo_search_comparison()
