# Merge Sort Implementation
# Demonstrates divide-and-conquer recursive sorting algorithm
from typing import List, Any, Callable, Optional


def merge_sort(items: List[Any], key: Optional[Callable] = None, reverse: bool = False) -> List[Any]:
    # Args:
    # items: List of items to sort
    # key: Optional function to extract comparison value from each item
    # reverse: If True, sort in descending order
    #
    # Returns:
    # New sorted list (does not modify original)
    #
    # BASE CASE: A list with 0 or 1 elements is already sorted
    # (this is what stops the recursion from going forever)
    if len(items) <= 1:
        return items.copy()  # Return a copy to avoid accidentally modifying the original
    
    # DIVIDE: Split the list into two halves (divide and conquer approach)
    mid = len(items) // 2
    left_half = items[:mid]
    right_half = items[mid:]
    
    # CONQUER: Recursively sort both halves
    # The function calls itself! This is the key part of merge sort
    # Eventually these reach the base case above
    left_sorted = merge_sort(left_half, key, reverse)
    right_sorted = merge_sort(right_half, key, reverse)
    
    # COMBINE: Merge the two sorted halves back together
    # This is where the actual sorting happens
    return _merge(left_sorted, right_sorted, key, reverse)


def _merge(left: List[Any], right: List[Any], key: Optional[Callable] = None, reverse: bool = False) -> List[Any]:
    # Args:
    # left: First sorted list
    # right: Second sorted list
    # key: Function to extract comparison value
    # reverse: If True, merge in descending order
    #
    # Returns:
    # Merged sorted list
    result = []
    i = j = 0
    
    # Helper function to get comparison value
    def get_value(item):
        return key(item) if key else item
    
    # Compare elements from both lists and add smaller one to result
    while i < len(left) and j < len(right):
        left_value = get_value(left[i])
        right_value = get_value(right[j])
        
        # Determine which element should come first
        if reverse:
            # For descending order, take the larger value
            if left_value >= right_value:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            # For ascending order, take the smaller value
            if left_value <= right_value:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
    
    # Add any remaining elements from left list
    while i < len(left):
        result.append(left[i])
        i += 1
    
    # Add any remaining elements from right list
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result


def merge_sort_parts_by_price(parts: List[dict], ascending: bool = True) -> List[dict]:
    # Convenience function to sort PC parts by price using merge sort
    #
    # Args:
    # parts: List of part dictionaries with 'price' key
    # ascending: If True, sort cheapest first; if False, most expensive first
    #
    # Returns:
    # Sorted list of parts
    return merge_sort(parts, key=lambda p: p.get('price', 0), reverse=not ascending)


def merge_sort_parts_by_name(parts: List[dict]) -> List[dict]:
    # Convenience function to sort PC parts alphabetically by name
    #
    # Args:
    # parts: List of part dictionaries with 'name' key
    #
    # Returns:
    # Alphabetically sorted list of parts
    return merge_sort(parts, key=lambda p: p.get('name', '').lower())
