"""
Tests for src/samples/sample.py
"""

from src.samples.sample import Sample
import pytest

@pytest.mark.parametrize("path,expected_output", [
    ("plaintext1.txt", b"Adam.\n"),
    ("plaintext2.txt", b"trivial\n2\n"),
    ("plaintext3.txt", b"JPG\x04\x08\n")
])
def test_load_file(path: str, expected_output: bytes):

    sample = Sample("tests/samples/sample_inputs/" + path)

    sample.load_file()

    assert expected_output == sample._input
