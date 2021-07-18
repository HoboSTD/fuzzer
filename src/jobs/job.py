
from threading import Thread
from subprocess import run, CompletedProcess
from src.fuzzer import Fuzzer

class Job():
    """
    Handles the running of a process with a given input.
    """

    def __init__(self, fuzzer: Fuzzer, binary_path: str) -> None:
        self._fuzzer: Fuzzer = fuzzer
        self._binary_path: str = binary_path

    def start(self):
        """
        Starts the fuzzing process.
        """

        self._thread = Thread(target=self.main, args=())
        self._thread.start()

    def main(self):
        """
        Retrieves inputs from the fuzzer until the fuzzer stops giving us inputs.
        """

        input = self._fuzzer.fuzz()
        while input != None:

            returncode = self.execute(input)

            self._fuzzer.analyse(returncode, input)

            input = self._fuzzer.fuzz()

    def execute(self, input: bytes) -> int:
        """
        Runs the binary with the given output and returns the program's exit code.
        """
        
        return run(["./" + self._binary_path], input=input, capture_output=True).returncode
