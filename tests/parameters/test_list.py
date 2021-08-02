"""
Tests for src/parameters/list.py
"""

from random import seed
from src.parameters.string import String
from src.parameters.integer import Integer
from src.parameters.list import FuzzingList

def test_init():

    my_list = FuzzingList(b"[1, some string, 3, 4]")
    exp_list = [Integer(), String(b" some string"), Integer(), Integer()]

    assert len(my_list._list) == len(exp_list)
    for i in range(0, len(exp_list)):
        assert type(my_list._list[i]) == type(exp_list[i])

def test_get_mutation():

    seed(1)
    my_list = FuzzingList(b"[1, some string, 3, 4]")

    assert my_list.get_mutation() == b"[-496651787, some string,-802700079,21771324]"
