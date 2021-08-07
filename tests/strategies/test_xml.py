"""
Tests for src/strategies/xml.py
"""

from typing import List
import pytest
from src.strategies.xml import XMLAttribute, XMLTag, parse_xml

@pytest.mark.parametrize("attribute,expname,expvalue", [
    (b"name=\"test\"", b"name", b"test"),
    (b"id=\"#lol\"", b"id", b"#lol"),
    (b"src", b"src", b""),
    (b"name='test'", b"name", b"test"),
    (b"id='#lol'", b"id", b"#lol"),
])
def test_xml_attribute_creation(attribute: bytes, expname: bytes, expvalue: bytes):
    
    xmlAttribute = XMLAttribute(attribute)

    assert expname == xmlAttribute._name
    assert expvalue == xmlAttribute._value

@pytest.mark.parametrize("xml,exptag,expattributes,expchildren", [
    (b"<head></head>", b"head", [], []),
    (b"<div><hello></hello></div>", b"div", [], []),
    (b"<div id=\"#lol\" src onerror=\"test\"></div>", b"div", [XMLAttribute(b"id=\"#lol\""), XMLAttribute(b"src"), XMLAttribute(b"onerror=\"test\"")], []),
    (b"<div test=\"xd\"><a href=\"xd\"></a></div>", b"div", [XMLAttribute(b"test=\"xd\"")], []),
])
def test_xml_tag_creation(xml: bytes, exptag: bytes, expattributes: List[XMLAttribute], expchildren: List[XMLTag]):

    xmlTag = XMLTag(xml)

    assert exptag == xmlTag._tag
    assert len(expattributes) == len(xmlTag._attributes)
    for i in range(0, len(expattributes)):
        print(xmlTag._attributes[i]._attribute)
        assert expattributes[i] == xmlTag._attributes[i]
    assert len(expchildren) == len(xmlTag._children)
    for i in range(0, len(expchildren)):
        assert expchildren[i] == xmlTag._children[i]

def test_parse_xml_1():

    xml = b"<html><head><a></a></head><body><p></p></body></html>"

    xmlTag = parse_xml(xml)

    expA = XMLTag(b"<a></a>")
    expP = XMLTag(b"<p></p>")

    expHead = XMLTag(b"<head></head>")
    expHead._children = [expA]
    expBody = XMLTag(b"<body></body>")
    expBody._children = [expP]

    expTag = XMLTag(b"<html></html>")
    expTag._children = [expHead, expBody]

    assert expTag == xmlTag
    assert xmlTag.get_xml() == xml

def test_parse_xml_2():

    xml = b"<html><head><a href=\"https://www.google.com\"></a></head></html>"

    xmlTag = parse_xml(xml)

    expA = XMLTag(b"<a href=\"https://www.google.com\"></a>")
    expHead = XMLTag(b"<head></head>")
    expHead._children = [expA]
    expTag = XMLTag(b"<html></html>")
    expTag._children = [expHead]

    assert expTag == xmlTag
    assert expTag.get_xml() == xml

def test_parse_xml_3():

    xml = b"<html><head><link href=\"http://somewebsite.com\" /></head><body><h1></h1></body><div id=\"#lol\"><a href=\"http://google.com\"></a></div><tail><a href=\"http://bing.com\"></a></tail></html>"

    xmlTag = parse_xml(xml)

    print(xmlTag.get_xml())
    assert xmlTag.get_xml() == xml

def test_xml_fuzz():


    xml = b"<html><head><a href=\"https://www.google.com\"></a></head><link a=\"test\" /></html>"
    xmlTag = parse_xml(xml)

    for _ in range(1, 50):
        print(xmlTag.fuzz())

    assert 1 == 0
