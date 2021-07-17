"""
Tests for src/samples/plaintext.py
"""

from src.samples.plaintext import PlainText

def test_keywords_returned():

    plaintext = PlainText("tests/samples/sample_inputs/plaintext1.txt")

    assert [b"\n", b"\x00", b"\r\n", b"\t", b"\b", b"%s"] == plaintext.get_keywords()
