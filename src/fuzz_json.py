from fuzzer import Fuzzer
import json
import enum
from pwn import *
from thread import *
import copy

class json_methods(enum.Enum):
    BUFFER_OVERFLOW = "a" * 9999
    FORMAT_STRING = "%x"

class fuzz_json(Fuzzer):
    def __init__(self, file):
        super().__init__(file)
        self._format_string_limit = 999
        self._large_mutation = False
        self._infinite_mutation = False
        self._methods = []
        self._bytes_list = ["%s", "a", "\0", "\n"]
        self._bad_bytes = self.generate_bad_bytes()
        for method in json_methods:
            self._methods.append(method.value)
        try:
            self._json = json.loads(self._file)
        except:
            self._json = {}

    def generate_bad_bytes(self):
        bad_bytes_list = []
        i = 0
        while i < 128:
            if i < 48 or i > 122:
                bad_bytes_list.append(chr(i))
            i += 1
        bad_bytes_list += self._bytes_list
        return bad_bytes_list

    def mutate_str(self, string):
        str_list = list(string)
        ret = ""
        size = random.randint(1, len(string)+5)
        targets = []
        while len(targets) < size:
            random_target = random.randint(0, len(string)+5)
            if random_target not in targets:
                targets.append(random_target)
        for i in targets:
            random_bad_byte = random.randint(0, len(self._bad_bytes)-1)
            if i >= len(str_list):
                str_list.append(self._bad_bytes[random_bad_byte])
            else:
                str_list[i] = self._bad_bytes[random_bad_byte]
        return ret.join(str_list)

    
    def mutate_infinitely(self):
        json_copy = copy.deepcopy(self._json)
        random_key = random.choice(i for i in json_copy)
        random_json = json_copy[random_key]
        min = -2147483648
        max = 2147483648
        if isinstance(random_json, int):
            radnom_json = random.randint(min, max)
        if isinstance(random_json, str):
            random_json = self.mutate_str(random_json)
        if isinstance(random_json, list):
            random_index = random.randint(0, len(random_json)-1)
            random_element = random_json[random_index]
            if isinstance(random_element, str):
                random_json[random_index] = self.mutate_str(random_element)
            elif isinstance(random_element, int):
                random_json[random_index] = random.randint(min, max)
        return json.dumps(json_copy)



    def mutate(self):
        methods = copy.deepcopy(self._methods)
        Thread.get_instance()._semaphoreA.acquire()
        if self._methods != []:
            copy_json = copy.deepcopy(self._json)
            method = methods.pop(0)
            for x in copy_json:
                copy_json[x] = method
            Thread.get_instance()._semaphoreA.release()
            return json.dumps(copy_json)
        else:
            random_index = random.randint(0, len(self._bytes_list)-1)
            append_byte = self._bytes_list[random_index]
            stop = False
            for x in self._json:
                key = self._json[x]
                if isinstance(key, str):
                    if stop == False and key < 200:
                        stop = True
                    key = key + append_byte
                if isinstance(key, int):
                    if key == 0:
                        key = 1
                    if stop == False and len(str(key)) < 20:
                        stop = True
                    key = key*-2
                if isinstance(key, list):
                    for y in range(0, len(key)):
                        if isinstance(key[y], str):
                            if len(key[y]) < 200:
                                if stop == False:
                                    stop = True
                                key[y] = key[y] + append_byte
                        if isinstance(key[y], int):
                            if key[y] == 0:
                                key[y] = 1
                            if len(str(key[y])) < 20:
                                if stop == False:
                                    stop = True
                                key[y] = key[y]*-2
                    if len(key) < 1000:
                        sqrt = (100 - len(key))//2
                        for i in range(0, sqrt):
                            key.append("a")
                        for i in range(sqrt, 1000):
                            key.append(random.randint(-10, 10))
            if stop == False and self._large_mutation == False:
                self._large_mutation = True
                for i in range(0, 50):
                    self._json[f"add{i}"] = 'a'
                for i in range(50, 100):
                    self._json[f"add{i}"] = random.randint(-10, 10)
            elif stop == False and self._large_mutation:
                self._infinite_mutation = True
                f = open(self._file, "r")
                input = f.read().strip()
                self._json = json.loads(input)
            Thread.get_instance()._semaphoreA.release()
            return json.dumps(self._json) 


    def fuzz(self, mutate, stop):
        f = open(self._file, "r")
        input = f.read().strip()
        while True:
            if stop:
                Thread.get_instance().thread_result((mutate, 0), None)
                return
        
            (exit_code, ltrace_output) = Thread.get_instance().run_process(input)
            Thread.get_instance().thread_result((input, exit_code), ltrace_output)
            if exit_code != 0:
                return
            if self._infinite_mutation:
                self._file = self.mutate_infinitely()
            else:
                self._file = self.mutate()

    

        
