"""
Tests for src/inputs/input_type.py
"""

import pytest
from src.samples.sample_type import get_type, SampleType

@pytest.mark.parametrize("sample_path,expected_type", [
    ("csv1.txt", SampleType.CSV),
    ("csv2.txt", SampleType.CSV),
    ("jpg1.txt", SampleType.JPEG),
    ("json1.txt", SampleType.JSON),
    ("json2.txt", SampleType.JSON),
    ("plaintext1.txt", SampleType.PLAINTEXT),
    ("plaintext2.txt", SampleType.PLAINTEXT),
    ("plaintext3.txt", SampleType.PLAINTEXT),
    ("xml1.txt", SampleType.XML),
    ("xml2.txt", SampleType.XML),
    ("xml3.txt", SampleType.XML),
    ("csv1", SampleType.ELF),
    ("pdf1.pdf", SampleType.PDF)
])
def test_get_type(sample_path: str, expected_type: SampleType):
    
    type = get_type("tests/samples/sample_inputs/" + sample_path)

    assert expected_type == type
