"""
Yes.
"""

from src.parameters.string import String
# from src.parameters.list import FuzzingList
from src.parameters.integer import Integer

def get_parameter_type(base: bytes):
    """
    Returns the type that the base could be converted into.
    """

    if is_int(base):
        return Integer()
    # elif is_list(base):
    #    return FuzzingList(base)
    
    return String(base)

def is_int(base: bytes) -> bool:

    try:
        int(base.decode("utf-8"))
        return True
    except:
        return False

def is_list(base: bytes) -> bool:

    try:
        base = base.decode("utf-8")
        if base[0] != "[" or base[-1] != "]":
            return False
        # maybe check for number of ,'s?
        # what about 1 item lists?
        return True
    except:
        return False
