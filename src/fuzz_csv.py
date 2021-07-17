from fuzzer import Fuzzer
from thread import *
import copy

class fuzz_csv(Fuzzer):
    def __init__(self, file):
        super.__init__(file)
        self._lines = self.file.split("\n")
        self._n_commas = self._lines[0].count(",")
        self._n_values = self._n_commas+1
        self._methods = ["single_buffer_overflow, multi_buffer_overflow. format_string"]

    def single_buffer_overflow(self, payload):
        for i in range(0, 999):
            append_payload = "\n"
            for j in range(0, self._n_commas):
                append_payload += 'a,'
            append_payload += 'a'
        payload += append_payload
        return payload

    def multi_buffer_overflow(self, payload):
        append_payload = "\n"
        for i in range(0, self._n_commas):
            append_payload += 'a'*99 + ','
        append_payload += 'a'*100
        payload += append_payload
        return payload

    def format_string(self, payload):
        payload += '%s'
        return payload

    def mutator(self, input, mutation):
        payload = ''
        mutation = str(mutation)
        for x in range(0, self._n_commas):
            payload += mutation + ','
        payload += mutation
        return payload

    def fuzz_by_line(self, mutate, i, payload, methods, stop):
        if i == len(self._lines):
            return
        if stop():
            Thread.get_instance().thread_result((mutate, 0), None)
            return
        payload[i] = self._lines[i]
        methods = copy.deep(self._methods)
        while methods != []:
            method = methods.pop(0)
            if method == "multi_buffer_overflow":
                payload[i] = self.mutator(payload[i], "a"*99)
            elif method == "format_string":
                payload[i] = self.mutator(payload[i], "%x")
            else:
                pass
            new_line = "\n".join(payload)
            (exit_code, ltrace_output) = Thread.get_instance().run_process(new_line)
            Thread.get_instance().thread_result((payload, exit_code), ltrace_output)
            if exit_code != 0:
                return
        self.fuzz_by_line(mutate, i+1, payload, methods, stop)
        Thread.get_instance().thread_result((payload, exit_code), ltrace_output)
        return

    def fuzz_payload(self, mutate, stop):
        if stop():
            Thread.get_instance().thread_result(("", 0), None)
            return
        f = open(self._file, "r")
        payload = f.read().strip()
        methods = copy.deepcopy(self._methods)
        while methods != []:
            method = methods.pop(0)
            if method == "single_buffer_overflow":
                payload = "A"*9999
            elif method == "format_string":
                payload = "%x"
            else:
                pass
            (exit_code, ltrace_output) = Thread.get_instance().run_process(payload)
            Thread.get_instance().thread_result((payload, exit_code), ltrace_output)
            if exit_code != 0:
                return


    def fuzz(self, mutate, stop):
        if stop():
            Thread.get_instance().thread_result((mutate, 0), None)
            return
        empty = ""
        (exit_code, ltrace_output) = Thread.get_instance().run_process(empty)
        Thread.get_instance().thread_result((empty, exit_code), ltrace_output)
        if exit_code != 0:
            return
        f = open(self._file, "r")
        input = f.read().strip()

        methods = copy.deepcopy(self._methods)
        while methods != []:
            method = methods.pop(0)
            if method == "single_buffer_overflow":
                payload = self.single_buffer_overflow(input)
            elif method == "multi_buffer_overflow":
                payload = self.multi_buffer_overflow(input)
            elif method == "format_string":
                payload = self.format_string(input)
            else:
                pass

            (exit_code, ltrace_output) = Thread.get_instance().run_process(payload)
            Thread.get_instance().thread_result((payload, exit_code), ltrace_output)
            if exit_code != 0:
                return
        self.fuzz_payload(mutate, stop)
        lines = self._lines
        methods = copy.deepcopy(self._methods)
        self.fuzz_by_line(mutate, stop, 0, lines, methods)



        
