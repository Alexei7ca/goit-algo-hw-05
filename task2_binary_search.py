from typing import List, Tuple, Optional

def binary_search_ceil(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    """
    Performs binary search on a sorted list of floats.
    Returns: (number_of_iterations, ceiling_value)
    The ceiling value is the smallest element >= target.
    """
    n = len(arr)
    low = 0
    high = n - 1
    iterations = 0
    ceiling = None

    while low <= high:
        iterations += 1
        # Calculate mid index avoiding overflow
        mid = low + (high - low) // 2
        
        if arr[mid] == target:
            # Exact match found. This is the ceiling.
            ceiling = arr[mid]
            return iterations, ceiling
        elif arr[mid] < target:
            # Target is larger, search in the right half
            low = mid + 1
        else: # arr[mid] > target
            # Current element is a potential ceiling. Store it and search the left half
            # to find a smaller (but still valid) ceiling candidate.
            ceiling = arr[mid]
            high = mid - 1
            
    # Return the iteration count and the smallest element >= target found
    return iterations, ceiling

def run_task2():
    test_array = [1.5, 3.2, 5.0, 7.8, 9.1, 10.3, 12.0]
    print(f"Array: {test_array}")

    # Case 1: Exact match (7.8)
    target1 = 7.8
    iters1, ceil1 = binary_search_ceil(test_array, target1)
    print(f"Target: {target1}, Result: (Iters: {iters1}, Ceiling: {ceil1})")

    # Case 2: No exact match, but an existing ceiling (5.0)
    target2 = 4.0
    iters2, ceil2 = binary_search_ceil(test_array, target2)
    print(f"Target: {target2}, Result: (Iters: {iters2}, Ceiling: {ceil2})")

    # Case 3: Target greater than all elements (No ceiling)
    target3 = 15.0
    iters3, ceil3 = binary_search_ceil(test_array, target3)
    print(f"Target: {target3}, Result: (Iters: {iters3}, Ceiling: {ceil3})")

    # Case 4: Target smaller than all elements (1.5 is the ceiling)
    target4 = 0.5
    iters4, ceil4 = binary_search_ceil(test_array, target4)
    print(f"Target: {target4}, Result: (Iters: {iters4}, Ceiling: {ceil4})")

if __name__ == "__main__":
    run_task2()