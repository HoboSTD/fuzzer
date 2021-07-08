"""
An example of how tests work.
"""

from src.example import read_file


def test_read_file():
    assert read_file("tests/example_test_file.txt") == "blah\nblah\nblah"
