"""
Tests for fuzzer/parameters/integer.py
"""

from random import seed
from src.parameters.integer import Integer

def test_get_mutation():

    seed(1)
    
    integer = Integer()

    assert integer.get_mutation() == b"-496651787"
    assert integer.get_mutation() == b"-802700079"
    assert integer.get_mutation() == b"21771324"
    assert integer.get_mutation() == b"-567284855"
    assert integer.get_mutation() == b"1054135675"
    assert integer.get_mutation() == b"856807587"
