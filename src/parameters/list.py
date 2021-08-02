"""
Generates random lists that are used during during fuzzing.
"""

from typing import List
from src.parameters.parameter import Parameter
from src.parameters.parameter_type import get_parameter_type


class FuzzingList(Parameter):
    
    def __init__(self, base: bytes) -> None:
        self._base = base[1:-1]
        items = self._base.split(b",")
        self._list: List[Parameter] = []
        for item in items:
            self._list.append(get_parameter_type(item))

    def get_mutation(self) -> bytes:
        mutation = b"["
        for i in range(0, len(self._list)):
            if i != 0:
                mutation += b","
            mutation += self._list[i].get_mutation()
        mutation += b"]"

        return mutation