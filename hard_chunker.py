
    # before calling this with optional arg list_of_indexes, 
    # somehow analyze the iterable to provide list_of_indexes

def hard_chunk_serializable(serializable, chunk_size, list_of_indexes=None):
    """
    Breaks a serializable object into smaller chunks of a given size,
    optionally starting at specified indices.

    Args:
        serializable (sequence): The input serializable object (e.g., list, string, tuple).
        chunk_size (int): The maximum size of each chunk.
        list_of_indexes (list of int, optional): List of starting indices for chunks.
            If None, chunks are created sequentially based on chunk_size.

    Yields:
        The chunks of the input object.

    Raises:
        TypeError: If an index in list_of_indexes is not an integer.
        IndexError: If an index is out of bounds for the serializable object.
        ValueError: If chunk_size is not a positive integer.
    """
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("'chunk_size' must be a positive integer.")

    if list_of_indexes is None:
        # Default behavior: chunk sequentially based on chunk_size
        for i in range(0, len(serializable), chunk_size):
            yield serializable[i:i + chunk_size]
    else:
        # Custom chunk boundaries based on list_of_indexes
        for index in list_of_indexes:
            if not isinstance(index, int):
                raise TypeError(f"Index '{index}' is not an integer.")
            if index < 0 or index >= len(serializable):
                raise IndexError(
                    f"Index '{index}' is out of bounds for the serializable of length {len(serializable)}."
                )
            yield serializable[index:index + chunk_size]


if __name__ == '__main__':
    # Test cases for hard_chunk_serializable

    # Test Case 1: Default Sequential Chunking with a List
    data1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    chunk_size1 = 3

    print("Test Case 1: Default Sequential Chunking with a List")
    chunks1 = list(hard_chunk_serializable(data1, chunk_size1))
    for idx, chunk in enumerate(chunks1):
        print(f"Chunk {idx + 1}: {chunk}")
    print()

    # Test Case 2: Custom Indices with Overlapping Chunks
    data2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    chunk_size2 = 3
    list_of_indexes2 = [0, 2, 5]

    print("Test Case 2: Custom Indices with Overlapping Chunks")
    chunks2 = list(hard_chunk_serializable(data2, chunk_size2, list_of_indexes2))
    for idx, chunk in enumerate(chunks2):
        print(f"Chunk {idx + 1}: {chunk}")
    print()

    # Test Case 3: String Input with Custom Indices
    data3 = "Hello, World!"
    chunk_size3 = 5
    list_of_indexes3 = [0, 7]

    print("Test Case 3: String Input with Custom Indices")
    chunks3 = list(hard_chunk_serializable(data3, chunk_size3, list_of_indexes3))
    for idx, chunk in enumerate(chunks3):
        print(f"Chunk {idx + 1}: '{chunk}'")
    print()

    # Test Case 4: List of Dictionaries with Custom Indices
    data4 = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 3, 'name': 'Charlie'},
        {'id': 4, 'name': 'Diana'},
        {'id': 5, 'name': 'Evan'}
    ]
    chunk_size4 = 2
    list_of_indexes4 = [0, 3]

    print("Test Case 4: List of Dictionaries with Custom Indices")
    chunks4 = list(hard_chunk_serializable(data4, chunk_size4, list_of_indexes4))
    for idx, chunk in enumerate(chunks4):
        print(f"Chunk {idx + 1}: {chunk}")
    print()

    # Test Case 5: Error Handling - Non-integer Index
    data5 = [1, 2, 3, 4, 5]
    chunk_size5 = 2
    list_of_indexes5 = [0, 'a', 4]  # 'a' is not an integer

    print("Test Case 5: Error Handling - Non-integer Index")
    try:
        chunks5 = list(hard_chunk_serializable(data5, chunk_size5, list_of_indexes5))
    except TypeError as e:
        print(f"Caught exception: {e}")
    print()

    # Test Case 6: Error Handling - Index Out of Bounds
    data6 = [1, 2, 3, 4, 5]
    chunk_size6 = 2
    list_of_indexes6 = [0, 4, 5]  # Index 5 is out of bounds

    print("Test Case 6: Error Handling - Index Out of Bounds")
    try:
        chunks6 = list(hard_chunk_serializable(data6, chunk_size6, list_of_indexes6))
    except IndexError as e:
        print(f"Caught exception: {e}")
    print()

    # Test Case 7: Error Handling - Negative Chunk Size
    data7 = [1, 2, 3, 4, 5]
    chunk_size7 = -1

    print("Test Case 7: Error Handling - Negative Chunk Size")
    try:
        chunks7 = list(hard_chunk_serializable(data7, chunk_size7))
    except ValueError as e:
        print(f"Caught exception: {e}")
    print()
