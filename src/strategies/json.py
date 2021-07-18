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

        self._large_mutation_done = False
        self._infinite_mutation = False

        self._methods = []
        for method in json_methods:
            self._methods.append(method.value)

    def get_keywords(self) -> List[bytes]:
        return [b"%s", b"a", b"\0", b"\n"]

    def set_sample(self, sample: Sample) -> None:
        super().set_sample(sample)
        # split it up into new lines

        self.reset_json()

    def get_input(self) -> bytes:
        mutated = ""
        if self._infinite_mutation:
            mutated = self.mutate_infinitely()
        else:
            mutated = self.mutate()

        return bytes(mutated, 'utf-8')

    def reset_json(self) -> None:
        try:
            self._json = json.loads(self._sample._input)
        except:
            self._json = {}
    
    def mutate_infinitely(self):
        json_copy = copy.deepcopy(self._json)
        rand_key = choice([i for i in json_copy])
        rand_val = json_copy[rand_key]

        min = -2147483648
        max = 2147483648

        if isinstance(rand_val, int):
            rand_val = randint(min, max)
        elif isinstance(rand_val, str):
            rand_val = self.mutate_str(rand_val)
        elif isinstance(rand_val, list):
            rand_index = randint(0, len(rand_val)-1)
            rand_list_val = rand_val[rand_index]
            if isinstance(rand_list_val, int):
                rand_val[rand_index] = randint(min, max)
            elif isinstance(rand_list_val, str):
                rand_val[rand_index] = self.mutate_str(rand_list_val)
        # change type too? done already using methods?

        json_copy[rand_key] = rand_val
        return json.dumps(json_copy)



    def mutate(self):
        #methods = copy.deepcopy(self._methods)
        #Thread.get_instance()._semaphoreA.acquire()

        # try overflow/fmt if we haven't already
        if self._methods != []:
            copy_json = copy.deepcopy(self._json)
            method_val = self._methods.pop(0)
            for key in copy_json:
                copy_json[key] = method_val
            #Thread.get_instance()._semaphoreA.release()
            return json.dumps(copy_json)
        else:
            rand_index = randint(0, len(self._bytes_list)-1)
            append_byte = self._bytes_list[rand_index]

            stop = False
            for key in self._json:
                val = self._json[key]
                if isinstance(val, str):
                    if len(val) < 200:
                        stop = True
                    self._json[key] = val + append_byte
                elif isinstance(val, int):
                    if val == 0:
                        val = 1
                    if len(str(val)) < 20:
                        stop = True
                    self._json[key] = val*-2
                elif isinstance(val, list):
                    for y in range(len(val)):
                        if isinstance(val[y], str):
                            if len(val[y]) < 200:
                                stop = True
                                val[y] = val[y] + append_byte
                        if isinstance(val[y], int):
                            if val[y] == 0:
                                val[y] = 1
                            if len(str(val[y])) < 20:
                                stop = True
                                val[y] = val[y]*-2
                    if len(val) < 1000:
                        sqrt = (100 - len(val))//2
                        for i in range(0, sqrt):
                            val.append("a")
                        for i in range(sqrt, 1000):
                            val.append(randint(-10, 10))
            
            if stop == False and self._large_mutation_done == False:
                self._large_mutation_done = True
                for i in range(0, 50):
                    self._json[f"add{i}"] = 'a'
                for i in range(50, 100):
                    self._json[f"add{i}"] = randint(-10, 10)
            elif stop == False and self._large_mutation_done:
                self._infinite_mutation = True
                self.reset_json()
            #Thread.get_instance()._semaphoreA.release()
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
            random_bad_byte = randint(0, len(self._bad_bytes)-1)
            if i >= len(str_list):
                str_list.append(self._bad_bytes[random_bad_byte])
            else:
                str_list[i] = self._bad_bytes[random_bad_byte]
        return ret.join(str_list)
