"""
Core module for the backend.
"""

# Dependencies
from src.load import LoadInvertedIndex
from src.secondary_memory_write import SinglePassInMemoryIndexing


def setup(input_filename: str, output_filename: str):
    """
    Setup the backend.
    """
    # Declare class
    load_inverted_index = LoadInvertedIndex(input_filename)
    # Load the inverted index
    load_inverted_index.load()
    # Get the inverted index
    inverted_index = load_inverted_index.get_inverted_index()
    spim = SinglePassInMemoryIndexing(output_filename)
    spim.add(inverted_index.get_hash())
    return inverted_index
