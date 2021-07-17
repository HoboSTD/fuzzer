"""
Tests for src/strategies/plaintext.py
"""

from src.strategies.plaintext import PlainText

def test_get_keywords():

    plaintext = PlainText()

    assert [b"\n", b"\x00", b"\r\n", b"\t", b"\b", b"%s"] == plaintext.get_keywords()
