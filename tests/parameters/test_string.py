"""
Tests for fuzzer/parameters/string.py
"""

from random import seed
from src.parameters.string import String

def test_get_mutation():

    seed(1)
    base = b"trivial"
    string = String(base)

    # takes 142 iterations before the overflow string is generated
    for _ in range(0, 142):
        assert string.get_mutation() == base

    assert string.get_mutation() == b"%s" * 1000
