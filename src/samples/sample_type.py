"""
Functions for checking the type of the file given.
"""

from typing import List
from magic import from_file
from enum import Enum
import json

class SampleType(Enum):
    UNKNOWN = 0
    PLAINTEXT = 1
    CSV = 2
    JSON = 3
    XML = 4
    JPEG = 5
    ELF = 6
    PDF = 7

def get_type(sample_path: str) -> SampleType:
    """
    Returns the file type of the given sample.
    """

    guess = from_file(sample_path)

    if is_csv(guess):
        return SampleType.CSV
    elif is_json(sample_path):
        return SampleType.JSON
    elif is_xml(guess):
        return SampleType.XML
    elif is_jpeg(guess):
        return SampleType.JPEG
    elif is_elf(guess):
        return SampleType.ELF
    elif is_pdf(guess):
        return SampleType.PDF
    elif is_plaintext(guess):
        return SampleType.PLAINTEXT
    else:
        return SampleType.UNKNOWN

def is_plaintext(guess: str) -> bool:

    return matches_in_guess(["ASCII text", "data"], guess)

def is_csv(guess: str) -> bool:

    return matches_in_guess(["CSV text"], guess)

'''
def is_json(guess: str) -> bool:

    return matches_in_guess(["JSON data"], guess)
'''

def is_json(sample_path: str) -> bool:
    try:
        f = open(sample_path)
        json_object = json.load(f)
    except ValueError:
        return False
    
    return True

def is_xml(guess: str) -> bool:

    return matches_in_guess(["HTML document"], guess)

def is_jpeg(guess: str) -> bool:

    return matches_in_guess(["JPEG image data"], guess)

def is_elf(guess: str) -> bool:

    return matches_in_guess(["ELF"], guess)

def is_pdf(guess: str) -> bool:

    return matches_in_guess(["pdf"], guess)

def matches_in_guess(matches: List[str], guess: str) -> bool:
    """Returns true if there are any matches that are in the given guess."""

    guess = guess.lower()

    for match in matches:
        if match.lower() in guess:
            return True
