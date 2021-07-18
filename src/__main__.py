from src.harness import Harness
from sys import argv

if len(argv) != 3:
    print("Usage: ./fuzzer binary binaryinput")
else:
    harness = Harness(argv[1], argv[2])
    harness.start()
