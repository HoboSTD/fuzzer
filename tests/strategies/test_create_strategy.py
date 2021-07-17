"""
Tests for src/strategy/create_strategy.py
"""

from src.strategies.create_strategy import get_strategy
from src.strategies.strategy import Strategy
from src.strategies.plaintext import PlainText
import pytest

@pytest.mark.parametrize("sample_path,expected_sample", [
    ("plaintext1.txt", PlainText),
    ("plaintext2.txt", PlainText),
    ("plaintext3.txt", PlainText)
])
def test_get_sample(sample_path: str, expected_sample: Strategy):

    sample_type = type(get_strategy("tests/samples/sample_inputs/" + sample_path))

    assert expected_sample == sample_type
