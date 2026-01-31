# Search Algorithms Module
# Demonstrates different search algorithms with time complexity analysis
from typing import List, Optional, Tuple, Callable
from .models import Component


def binary_search_by_price(components: List[Component], target_price: float) -> Optional[Component]:
    # Binary search to find component with price closest to target
    # REQUIRES: components list must be sorted by price
    #
    # Time Complexity: O(log n) - halves search space each iteration
    # Space Complexity: O(1) - only uses a few variables
    #
    # Args:
    # components: Sorted list of components (by price ascending)
    # target_price: Price to search for
    #
    # Returns:
    # Component closest to target price, or None if list is empty
    #
    # Example:
    # >>> parts = [CPU($100), CPU($200), CPU($300)]
    # >>> result = binary_search_by_price(parts, 250)
    # >>> result.price  # Returns $200 CPU (closest match)
    # Edge case: empty list
    if not components:
        return None
    
    # Single item - just return it, no need to search
    if len(components) == 1:
        return components[0]
    
    # Initialize pointers for binary search
    left = 0
    right = len(components) - 1
    
    # Keep track of the closest match we've found so far
    closest = components[0]
    min_diff = abs(components[0].price - target_price)
    
    # Keep dividing the search space in half until we've checked everything
    while left <= right:
        # Calculate middle index to check
        mid = (left + right) // 2
        current_price = components[mid].price
        current_diff = abs(current_price - target_price)
        
        # Is this component closer to the target price than our previous best?
        if current_diff < min_diff:
            min_diff = current_diff
            closest = components[mid]
        
        # Perfect match! No need to search further
        if current_price == target_price:
            return components[mid]
        
        # Current price is too low, search the right half (higher prices)
        elif current_price < target_price:
            left = mid + 1
        
        # Current price is too high, search the left half (lower prices)
        else:
            right = mid - 1
    
    return closest


def binary_search_exact(components: List[Component], target_price: float) -> Optional[Component]:
    # Binary search to find component with exact price match
    # REQUIRES: components list must be sorted by price
    #
    # Time Complexity: O(log n)
    # Space Complexity: O(1)
    #
    # Args:
    # components: Sorted list of components (by price ascending)
    # target_price: Exact price to search for
    #
    # Returns:
    # Component with exact price match, or None if not found
    if not components:
        return None
    
    left = 0
    right = len(components) - 1
    
    while left <= right:
        mid = (left + right) // 2
        current_price = components[mid].price
        
        if current_price == target_price:
            return components[mid]
        elif current_price < target_price:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def binary_search_range(components: List[Component], min_price: float, max_price: float) -> List[Component]:
    # Binary search to find all components within a price range
    # REQUIRES: components list must be sorted by price
    #
    # Time Complexity: O(log n + k) where k is number of results
    # Space Complexity: O(k) for results list
    #
    # Args:
    # components: Sorted list of components (by price ascending)
    # min_price: Minimum price (inclusive)
    # max_price: Maximum price (inclusive)
    #
    # Returns:
    # List of components within price range
    if not components or min_price > max_price:
        return []
    
    # Find first component >= min_price
    left_bound = _find_left_bound(components, min_price)
    
    if left_bound == len(components):
        return []  # All components are below min_price
    
    # Find last component <= max_price
    right_bound = _find_right_bound(components, max_price)
    
    if right_bound == -1:
        return []  # All components are above max_price
    
    # Return slice of components in range
    return components[left_bound:right_bound + 1]


def _find_left_bound(components: List[Component], target: float) -> int:
    # Find index of first component with price >= target
    # Helper function for range search
    #
    # Time Complexity: O(log n)
    left = 0
    right = len(components)
    
    while left < right:
        mid = (left + right) // 2
        if components[mid].price < target:
            left = mid + 1
        else:
            right = mid
    
    return left


def _find_right_bound(components: List[Component], target: float) -> int:
    # Find index of last component with price <= target
    # Helper function for range search
    #
    # Time Complexity: O(log n)
    left = -1
    right = len(components) - 1
    
    while left < right:
        mid = (left + right + 1) // 2
        if components[mid].price > target:
            right = mid - 1
        else:
            left = mid
    
    return right


def linear_search_by_price(components: List[Component], target_price: float) -> Optional[Component]:
    # Linear search to find component closest to target price
    # NO SORTING REQUIRED - works on any list
    #
    # Time Complexity: O(n) - checks every element
    # Space Complexity: O(1)
    #
    # Comparison with binary search:
    # - Binary: O(log n) but requires sorted list
    # - Linear: O(n) but works on unsorted list
    #
    # Use this when:
    # - List is small (n < 100)
    # - List is unsorted and sorting would be expensive
    # - Need to search only once
    #
    # Args:
    # components: List of components (any order)
    # target_price: Price to search for
    #
    # Returns:
    # Component closest to target price, or None if list is empty
    if not components:
        return None
    
    closest = components[0]
    min_diff = abs(components[0].price - target_price)
    
    # Check every component (LINEAR scan)
    for component in components:
        diff = abs(component.price - target_price)
        if diff < min_diff:
            min_diff = diff
            closest = component
    
    return closest


def compare_search_algorithms(components: List[Component], target_price: float) -> dict:
    # Compare binary search vs linear search performance
    # Demonstrates algorithmic complexity analysis
    #
    # Args:
    # components: List of components
    # target_price: Price to search for
    #
    # Returns:
    # Dictionary with comparison results and statistics
    import time
    
    # Linear search (works on unsorted)
    start = time.perf_counter()
    linear_result = linear_search_by_price(components, target_price)
    linear_time = time.perf_counter() - start
    
    # Sort for binary search
    start = time.perf_counter()
    sorted_components = sorted(components, key=lambda c: c.price)
    sort_time = time.perf_counter() - start
    
    # Binary search (requires sorted)
    start = time.perf_counter()
    binary_result = binary_search_by_price(sorted_components, target_price)
    binary_time = time.perf_counter() - start
    
    return {
        'list_size': len(components),
        'target_price': target_price,
        'linear_search': {
            'time_seconds': linear_time,
            'comparisons': len(components),  # Worst case
            'result': linear_result.name if linear_result else None
        },
        'binary_search': {
            'time_seconds': binary_time,
            'sort_time_seconds': sort_time,
            'total_time_seconds': binary_time + sort_time,
            'comparisons': len(components).bit_length(),  # log2(n)
            'result': binary_result.name if binary_result else None
        },
        'speedup': linear_time / binary_time if binary_time > 0 else 0,
        'analysis': _analyze_performance(len(components), linear_time, binary_time)
    }


def _analyze_performance(n: int, linear_time: float, binary_time: float) -> str:
    # Provide analysis of search performance
    #
    # Returns:
    # Human-readable analysis string
    speedup = linear_time / binary_time if binary_time > 0 else 1
    
    if n < 50:
        return f"Small dataset (n={n}): Difference minimal. Linear search acceptable."
    elif n < 200:
        return f"Medium dataset (n={n}): Binary search {speedup:.1f}x faster. Consider sorting."
    else:
        return f"Large dataset (n={n}): Binary search {speedup:.1f}x faster. Sorting recommended."


def search_components_by_attribute(
    components: List[Component],
    attribute: str,
    target_value: any,
    key_func: Optional[Callable] = None
) -> Optional[Component]:
    # Generic binary search by any comparable attribute
    # REQUIRES: components sorted by the specified attribute
    #
    # Time Complexity: O(log n)
    # Space Complexity: O(1)
    #
    # Args:
    # components: Sorted list of components
    # attribute: Attribute name to search by
    # target_value: Value to search for
    # key_func: Optional function to extract comparison value
    #
    # Returns:
    # Component with closest matching attribute value
    #
    # Example:
    # >>> # Search by wattage (power_draw)
    # >>> result = search_components_by_attribute(
    # ...     gpus, 'power_draw', 250,
    # ...     key_func=lambda c: c.attributes.get('power_draw', 0)
    # ... )
    if not components:
        return None
    
    # Default key function: get attribute from component
    if key_func is None:
        key_func = lambda c: c.attributes.get(attribute, 0)
    
    left = 0
    right = len(components) - 1
    closest = components[0]
    min_diff = abs(key_func(components[0]) - target_value)
    
    while left <= right:
        mid = (left + right) // 2
        current_value = key_func(components[mid])
        current_diff = abs(current_value - target_value)
        
        if current_diff < min_diff:
            min_diff = current_diff
            closest = components[mid]
        
        if current_value == target_value:
            return components[mid]
        elif current_value < target_value:
            left = mid + 1
        else:
            right = mid - 1
    
    return closest
