"""
Handles json inputs.
"""

from typing import List
from src.strategies.strategy import Strategy
from src.samples.sample import Sample

from enum import Enum
import json
import copy
from random import randint, choice

class json_methods(Enum):
    BUFFER_OVERFLOW = "a" * 8192
    FORMAT_STRING = "%s" * 32

class JsonStrategy(Strategy):

    def __init__(self) -> None:
        super().__init__()

        self._bytes_list = ["%s", "a", "\0", "\n"]
        self._bad_bytes = self.generate_bad_bytes() + self._bytes_list

        self._state = 0

        self._methods = []
        for method in json_methods:
            self._methods.append(method.value)

    def get_keywords(self) -> List[bytes]:
        return [b"%s", b"a", b"\0", b"\n"]

    def set_sample(self, sample: Sample) -> None:
        super().set_sample(sample)

        self.reset_json()

    def get_input(self) -> bytes:
        mutated = self.mutate_machine()

        return bytes(mutated, 'utf-8')

    def reset_json(self) -> None:
        try:
            self._json = json.loads(self._sample._input)
        except:
            self._json = {}
    


    def mutate_infinitely_recursive(self, rand_val):
        min = -2147483648
        max = 2147483648

        if isinstance(rand_val, int):
            rand_val = randint(min, max)
        elif isinstance(rand_val, str):
            rand_val = self.mutate_str(rand_val)
        elif isinstance(rand_val, list):
            rand_index = randint(0, len(rand_val)-1)
            rand_val[rand_index] = self.mutate_infinitely_recursive(rand_val[rand_index])
        # change type too? done already using "methods"?

        return rand_val

    def mutate_infinitely(self):
        json_copy = copy.deepcopy(self._json)
        rand_key = choice([i for i in json_copy])

        json_copy[rand_key] = self.mutate_infinitely_recursive(json_copy[rand_key])
        return json.dumps(json_copy)



    def mutate_machine(self):

        # try overflow/fmt if we haven't already
        if self._state == 0:
            copy_json = copy.deepcopy(self._json)
            method_val = self._methods.pop(0)
            for key in copy_json:
                copy_json[key] = method_val

            if len(self._methods) == 0:
                self._state = 1
                #print("NEW STATE", self._state)
            return json.dumps(copy_json)
        elif self._state == 1:
            append_byte = choice(self._bytes_list)
            found = False
            for key in self._json:
                val = self._json[key]
                if isinstance(val, str):
                    if len(val) < 200:
                        found = True
                    self._json[key] = val + append_byte
                elif isinstance(val, int):
                    if val == 0:
                        val = 1
                    if len(str(val)) < 20:
                        found = True
                    self._json[key] = val*-2
                elif isinstance(val, list):
                    for y in range(len(val)):
                        if isinstance(val[y], str):
                            if len(val[y]) < 200:
                                found = True
                                val[y] = val[y] + append_byte
                        if isinstance(val[y], int):
                            if val[y] == 0:
                                val[y] = 1
                            if len(str(val[y])) < 20:
                                found = True
                                val[y] = val[y]*-2
                    if len(val) < 1000:
                        sqrt = (100 - len(val))//2
                        for i in range(0, sqrt):
                            val.append("a")
                        for i in range(sqrt, 1000):
                            val.append(randint(-10, 10))
            if not found:
                self._state = 2
                #print("NEW STATE", self._state)
        elif self._state == 2:
            for i in range(0, 50):
                self._json[f"add{i}"] = 'a'
            for i in range(50, 100):
                self._json[f"add{i}"] = randint(-10, 10)

            self._state = 3
            #print("NEW STATE", self._state)
        elif self._state == 3:
            self.reset_json()

            self._state = 4
            #print("NEW STATE", self._state)
        elif self._state == 4:
            return self.mutate_infinitely()

        
        return json.dumps(self._json)

    def generate_bad_bytes(self):
        bad_bytes_list = []
        i = 0
        while i < 128:
            if i < 48 or i > 122:
                bad_bytes_list.append(chr(i))
            i += 1
        return bad_bytes_list

    def mutate_str(self, string):
        str_list = list(string)
        ret = ""
        size = randint(1, len(string)+5)
        targets = []
        while len(targets) < size:
            random_target = randint(0, len(string)+5)
            if random_target not in targets:
                targets.append(random_target)
        for i in targets:
            random_bad_byte = choice(self._bad_bytes)
            if i >= len(str_list):
                str_list.append(random_bad_byte)
            else:
                str_list[i] = random_bad_byte
        return ret.join(str_list)
