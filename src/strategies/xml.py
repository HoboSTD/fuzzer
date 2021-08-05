"""
Strategy for generating fuzzed xml input.
"""

import re
from typing import List, Tuple

from src.samples.sample import Sample
from src.strategies.strategy import Strategy

class XMLStrategy(Strategy):

    def __init__(self) -> None:
        super().__init__()

    def get_keywords(self) -> List[bytes]:
        return super().get_keywords()

    def set_sample(self, sample: Sample) -> None:
        return super().set_sample(sample)    

    def get_input(self) -> bytes:
        return super().get_input()

class XMLAttribute():
    
    _attribute: bytes = b""
    _name: bytes = b""
    _value: bytes = b""

    def __init__(self, attribute: bytes) -> None:
        self._attribute: bytes = attribute
        self.parse_name()
        self.parse_value()

    def parse_name(self) -> None:
        try:
            index = self._attribute.index(b"=")
            self._name = self._attribute[0:index]
        except:
            self._name = self._attribute

    def parse_value(self) -> None:
        try:
            index = self._attribute.index(b"=")
            self._value = self._attribute[index+1:].strip(b"\"\'")
        except:
            self._value = b""
    
    def get_xml(self) -> bytes:
        if self._name == b"/":
            return b""
        xml = self._name
        if self._value != b"":
            xml += b"=\""
            xml += self._value
            xml += b"\""
        return xml

    def __eq__(self, o: object) -> bool:
        if type(o) != XMLAttribute:
            return False
        
        o: XMLAttribute = o

        return self._name == o._name and self._value == o._value and self._attribute == o._attribute

class XMLTag():

    def __init__(self, xml: bytes, stupid_tag: bool = False) -> None:
        self._xml: bytes = xml
        self._stupid_tag: bool = stupid_tag
        self._tag: bytes = self.parse_tag(self._xml)
        self._attributes: List[XMLAttribute] = self.parse_attributes()
        self._children: List[XMLTag] = []

    def parse_tag(self, xml: bytes) -> bytes:
        firstOpenBracket = xml.index(b"<")
        firstClosedBracket = xml.index(b">")

        tag = xml[firstOpenBracket+1:firstClosedBracket]

        return tag.split(b" ")[0]

    def parse_attributes(self) -> bytes:
        # get the first <tag ...>
        firstOpenBracket = self._xml.index(b"<")
        firstClosedBracket = self._xml.index(b">")
        tag = self._xml[firstOpenBracket+1:firstClosedBracket]

        return [XMLAttribute(newAttribute) for newAttribute in tag.split(b" ")[1:]]

    def add_child(self, tag) -> None:
        self._children.append(tag)

    def get_xml(self) -> bytes:
        xml = b"<"
        xml += self._tag
        xml += self.get_attributes()
        if self._stupid_tag:
            xml += b"/>"
            return xml
        xml += b">"
        xml += self.get_children_xml()
        # add random garbage here when fuzzing because this is technically part of the xml.
        # xml += b"AAAAAAAAAAAAAAAAAAAAAAAAA"
        xml += b"</"
        xml += self._tag
        xml += b">"
        return xml

    def get_children_xml(self) -> bytes:
        xml = b""
        for child in self._children:
            xml += child.get_xml()
        return xml

    def get_attributes(self) -> bytes:
        xml = b""
        for attrib in self._attributes:
            xml += b" "
            xml += attrib.get_xml()
        return xml

    def __eq__(self, o: object) -> bool:
        if type(o) != XMLTag:
            return False

        o: XMLTag = o

        if self._tag != o._tag:
            return False
        if len(self._attributes) != len(o._attributes):
            print("a")
            return False
        for i in range(0, len(self._attributes)):
            if self._attributes[i] != o._attributes[i]:
                print("b")
                return False
        if len(self._children) != len(o._children):
            print("c")
            return False
        for i in range(0, len(self._children)):
            if self._children[i] != o._children[i]:
                print("d")
                return False

        return True

def parse_tag(xml: bytes) -> Tuple[bytes, bool]:
    print("parsing:",xml)
    openBracket = xml.index(b"<")
    closeBracket = xml.index(b">")

    stupidTag = xml[closeBracket - 1] == 47

    return xml[openBracket+1:closeBracket].split(b" ")[0], stupidTag

def parse_xml(xml: bytes) -> XMLTag:
    """Uses a stack to turn xml into a usable data structure."""

    stack: List[XMLTag] = []
    xml = xml.replace(b"\n", b"")

    i = 0
    while i < len(xml):
        current_tag, stupid_tag = parse_tag(xml[i:])
        print("tag:", current_tag)

        if stupid_tag:
            parent = stack.pop()
            print("popped:", parent._tag)
            j = xml.index(b"/>", i)
            tag = XMLTag(xml[i:j+2], True)
            parent.add_child(tag)
            stack.append(parent)
            i = j + 2
        elif current_tag[0] == 47:
            # it's a closing tag
            top = stack.pop()
            print("popped:", top._tag)
            if len(stack) == 0:
                return top
            parent = stack.pop()
            parent.add_child(top)
            stack.append(parent)
            i = xml.index(b">", i) + 1
        else:
            # find the next > after i
            j = xml.index(b">", i)
            # create a new tag using this substring
            tag = XMLTag(xml[i:j+1])
            stack.append(tag)
            i = j+1

    return stack[0]
