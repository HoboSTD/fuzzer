"""
Tests for src/samples/sample.py
"""

from src.samples.sample import Sample
from src.samples.create_sample import get_sample
from src.samples.plaintext import PlainText
import pytest

@pytest.mark.parametrize("sample_path,expected_sample", [
    ("plaintext1.txt", PlainText),
    ("plaintext2.txt", PlainText),
    ("plaintext3.txt", PlainText)
])
def test_get_sample(sample_path: str, expected_sample: Sample):

    sample_type = type(get_sample("tests/samples/sample_inputs/" + sample_path))

    assert expected_sample == sample_type
