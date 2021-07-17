
from pwn import *
import threading
import os
import sys
from fuzzer import Fuzzer


# https://www.google.com/search?channel=fs&client=ubuntu&q=python+threading
class Thread:
    __instance = None
    def get_instance():
        if Thread.__instance == None:
            Thread()
        return Thread.__instance

    def __init__(self, count):
        if Thread.__instance == None:
            Thread.__instance = self
            self._count = count
            self._code_flows = dict()
            self._code_flow_count = 0
            self._ltrace = False
            self._stop = False
            self._semaphoreA = threading.Semaphore(1)
        
        else:
            raise Exception("Thread must be a singleton class")

    def init_thread(self, fuzzer):
        self._stop = False
        f = open(fuzzer._file, "r")
        input = f.read().strip()
        for x in range(0, self._count):
            thread = threading.thread(target = fuzzer.fuzz, args =(input, lambda : self._stop))
            thread.start()
            print(f"Initialising thread: {thread.ident}")

    def run_default(self, progname, payload):
        p = process("./"+progname)
        p.sendline(payload)
        p.shutdown()
        ret = p.poll(block = True)
        p.stderr.close()
        p.stdout.close()
        return ret
        
    def run_ltrace(self, progname, payload):
        p = process("./"+progname)
        ltrace = process(["/usr/bin/ltrace", f"-p (p.pid", f"-s {999999}"])
        p.sendline(payload)
        p.shutdown()
        ret = p.poll(block = True)
        p.stderr.close()
        p.stdout.close()
        ltrace_output = []
        try:
            while True:
                ltrace_output.append(ltrace.recvline())
        except:
            pass
        ltrace.shutdown()
        ltrace.stderr.close()
        ltrace.stdout.close()
        return (ret, ltrace_output)

    def parse_ltrace(self, ltrace_output):
        code_flow = []
        original_output = []
        lib_call_pattern = ".*\("
        lib_result_pattern = "\=.*"
        for x in range(0, len(ltrace_output)-1):
            curr_call = ltrace_output[x].decode()
            original_output.append(curr_call)
            lib_call = re.search(lib_call_pattern, curr_call)
            lib_result = re.search(lib_result_pattern, curr_call)
            if lib_call is not None and lib_result is not None:
                lib_call = lib_call.group()
                lib_call = lib_call[:-1]
                lib_result = lib_result.group()
                lib_result = lib_result[2:]
                code_flow.append((lib_call, lib_result))
        return code_flow, original_output

    def thread_default(self, result):
        (input, exit_code) = result
        self._semaphoreA.acquire()
        if not self._stop:
            print("\n[*] Fuzzer results . . .")
            if (exit_code == 0):
                print("\n[*] No vulnerabilities detected")
            elif exit_code == -11:
                print("\n[*] Segmentation fault detected")
                print("\n[*] Input that caused the segmentation fault ...")
                print(f"\n[*] {input}")
                print(f"\n[*] Exit code: {exit_code}")
                f = open("bad.txt", "w+")
                f.write(input)
                f.close()
                self._stop = True
        self._semaphoreA.release()

    def thread_ltrace(self, result, ltrace_output):
        (input, exit_code) = result
        self._semaphoreA.acquire()
        if ltrace_output is not None:
            (ltrace_parse, original_ltrace) = self.parse_ltrace(ltrace_output)
            list_to_tuple = tuple(i[0] for i in ltrace_parse)
            
            if self._code_flows.get(list_to_tuple) is None:
                self._code_flows[list_to_tuple] = (1, input, original_ltrace)
            else:
                (count, payload, original_ltrace) = self._code_flows[list_to_tuple]
                self._code_flows[list_to_tuple] = (count+1, input, original_ltrace)
            self._code_flow_count += 1
        else:
            if not self._stop:
                print("\n[*] Fuzzer results . . .")
                if exit_code == 0:
                    print("\n[*] No vulnerabilities detected")
                elif exit_code == -11:
                    print("\n[*] Segmentation fault detected")
                    print("\n[*] Input that caused the segmentation fault ...")
                    print(f"\n[*] {input}")
                    print(f"[*] Exit code: {exit_code}")
                    f = open("bad.txt", "w+")
                    f.write(input)
                    f.close()
                    count = 1
                    cwd = os.getcwd()
                    trace_report_file = os.path.join(cwd, "trace", "trace.txt")
                    for x in self._code_flows:
                        file = os.path.join(cwd, "trace", str(count), "input.txt")
                        ltrace_file = os.path.join(cwd, "trace", str(count), "ltrace-output.txt")
                        os.makedirs(os.path.dirname(file), exist_ok=True)
                        sample_file = open(file, "w+")
                        sample_file.write(self._code_flows.get(x)[1])
                        sample_file.close()
                        code_path = ""
                        result_details = ""
                        for i in range(0, len(x)):
                            if i is not len(x)-1:
                                code_path += x[i] + " ---> "
                            else:
                                code_path += x[i]
                        result_details += f"""
                        [*] {count} : {code_path} x{self._code_flows.get(x)[0]}
                        """
                        count += 1
                    trace_report = f"""
                     ===== Trace Report =====

                    {result_details}

                    Ran a total of {self._code_flow_count} times

                     ===== Code path folders generated =====
                    """
                    os.makedirs(os.path.dirname(trace_report_file), exist_ok=True)
                    trace_file = open(trace_report_file)
                    trace_file.write(trace_report_file)
                    trace_file.close()
                    self._stop = True
            self._semaphoreA.release()
    Thread(len(os.sched.getaffinity(0)))
            

    def run_process(self, payload):
        progname = sys.argv[1]
        if self._ltrace:
            (exit_code, ltrace_output) = self.run_ltrace(progname, payload)
            return (exit_code, ltrace_output)
            
        else:
            exit_code = self.run_default(progname, payload)
            return (exit_code, None)

    def thread_result(self, result, ltrace_output):
        if self._ltrace:
            self.thread_ltrace(result, ltrace_output)
        else:
            self.thread_default(result)
            



    

        