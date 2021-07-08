from src.example import read_file
from sys import argv

if len(argv) != 3:
    print("Usage: ./fuzzer binary binaryinput")
else:
    print("Fuzzing go b" + "r"*1000)
