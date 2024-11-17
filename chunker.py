
def chunk_serializable(
    data,
    chunk_size,
    overlap=0,
    chunk_by='words',
    include_non_strings=False
):
    """
    Processes any serializable data structure to extract strings and chunk them.

    Parameters:
        data: The input data structure containing strings.
            - Can be any combination of nested lists, dictionaries, sets, tuples, etc.
        chunk_size (int): Maximum size of each chunk.
            - Must be a positive integer.
        overlap (int): Number of units to overlap between chunks.
            - Must be a non-negative integer.
        chunk_by (str): Unit to chunk by.
            - Options: 'characters' or 'words'.
        include_non_strings (bool): Whether to include non-string data by converting it to strings.
            - Default is False.

    Returns:
        List[str]: List of text chunks.

    Raises:
        ValueError: If invalid parameters are provided.

    Example Usage:
        data = [
            {"title": "Sample Document", "content": "This is a test."},
            {"section": ["More text here.", "Even more text."]}
        ]
        chunks = chunk_serializable(data, chunk_size=5, overlap=1, chunk_by='words')
        for chunk in chunks:
            print(chunk)
    """
    def extract_strings(data):
        """Recursively extracts strings from any data structure."""
        strings = []

        if isinstance(data, str):
            strings.append(data)
        elif include_non_strings and isinstance(data, (int, float, bool)):
            strings.append(str(data))
        elif isinstance(data, dict):
            for key, value in data.items():
                strings.extend(extract_strings(key))
                strings.extend(extract_strings(value))
        elif isinstance(data, (list, tuple, set)):
            for item in data:
                strings.extend(extract_strings(item))
        return strings

    # Validate parameters
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("'chunk_size' must be a positive integer.")
    if not isinstance(overlap, int) or overlap < 0:
        raise ValueError("'overlap' must be a non-negative integer.")
    if chunk_by not in ('characters', 'words'):
        raise ValueError("Invalid value for 'chunk_by'. Must be 'characters' or 'words'.")

    # Extract strings from the data structure
    text_list = extract_strings(data)

    # Concatenate all strings into one text
    text = ' '.join(text_list)

    # Tokenize the text based on the 'chunk_by' parameter
    if chunk_by == 'characters':
        tokens = list(text)
    elif chunk_by == 'words':
        tokens = text.split()

    # Handle empty tokens list
    if not tokens:
        return []

    chunks = []
    step = max(chunk_size - overlap, 1)

    for i in range(0, len(tokens), step):
        chunk_tokens = tokens[i:i + chunk_size]
        if chunk_by == 'characters':
            chunk = ''.join(chunk_tokens)
        else:  # 'words'
            chunk = ' '.join(chunk_tokens)
        chunks.append(chunk)

    return chunks

if __name__ == '__main__':
    # Test Case 1: List of dictionaries containing strings and integers
    data1 = [
        {"id": 1, "text": "First item", "value": 10},
        {"id": 2, "text": "Second item", "value": 20},
        {"id": 3, "text": "Third item", "value": 30},
        {"id": 4, "description": "Fourth item with additional description.", "value": 40}
    ]

    print("Test Case 1: List of dictionaries with strings and integers\n")
    chunks1 = chunk_serializable(
        data1,
        chunk_size=6,
        overlap=2,
        chunk_by='words',
        include_non_strings=True
    )
    for i, chunk in enumerate(chunks1):
        print(f"Chunk {i + 1}:\n{chunk}\n")

    # Test Case 2: HTML page as a string
    data2 = """
    <html>
        <head>
            <title>Sample HTML Page</title>
        </head>
        <body>
            <h1>Welcome to the Sample Page</h1>
            <p>This is a paragraph with <a href="#">a link</a> inside.</p>
            <p>Another paragraph with <strong>bold text</strong> and <em>italic text</em>.</p>
            <!-- This is a comment that should not be visible -->
        </body>
    </html>
    """

    print("Test Case 2: HTML page\n")
    chunks2 = chunk_serializable(
        data2,
        chunk_size=100,
        overlap=20,
        chunk_by='characters'
    )
    for i, chunk in enumerate(chunks2):
        print(f"Chunk {i + 1}:\n{chunk}\n")


def test_chunk_list_of_dicts():
    # List of dictionaries containing integers and strings
    data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
        {"id": 4, "name": "Diana"},
        {"id": 5, "name": "Eve"}
    ]
    chunk_size = 2
    overlap = 0
    chunk_by = "words"
    include_non_strings = True

    # Expected output based on current function logic
    expected = [
        "id 1 name Alice",
        "id 2 name Bob",
        "id 3 name Charlie",
        "id 4 name Diana",
        "id 5 name Eve"
    ]

    result = chunk_serializable(
        data,
        chunk_size=chunk_size,
        overlap=overlap,
        chunk_by=chunk_by,
        include_non_strings=include_non_strings
    )
    assert result == expected, f"Test failed! Expected: {expected}, Got: {result}"
    print("Test for list of dictionaries passed.")



def test_chunk_html_string():
    # HTML string
    html_string = "<html><head><title>Test</title></head><body><p>Hello, world!</p></body></html>"
    chunk_size = 20

    # Expected output: chunks of 20 characters
    expected = [
        "<html><head><title>",
        "Test</title></head><",
        "body><p>Hello, worl",
        "d!</p></body></html>"
    ]

    result = list(chunk_serializable(html_string, chunk_size))
    assert result == expected, f"Test failed! Expected: {expected}, Got: {result}"
    print("Test for HTML string passed.")


if __name__ == "__main__":
    test_chunk_list_of_dicts()
    test_chunk_html_string()