from random import randint
from sys import maxsize

def bitflip(b: bytes) -> bytes:
    """
    Invert 1 to 4 consecutive bits
    """
    
    b = bytearray(b)
    n = randint(1, 4)
    start = randint(0, len(b)*8 - n)

    for i in range(start, start+n):
        base = int(i // 8)
        shift = int(i % 8)
        b[base] ^= (1 << (7-shift))
    return bytes(b)

def byteflip(b: bytes) -> bytes:
    """
    Invert 1 to 4 consecutive bytes
    """
    
    b = bytearray(b)
    n = randint(1, min(4, len(b)))
    start = randint(0,  len(b) - n)

    for i in range(start, start+n):
        b[i] ^= 0xFF
    return bytes(b)

def arithmetic(b: bytes) -> bytes:
    """
    Performs addition and subtraction of -35 to 35 on 1 to 4 consecutive bytes
    """
    
    b = bytearray(b)
    n = randint(1, min(4, len(b)))
    start = randint(0,  len(b) - n)

    for i in range(start, start+n):
        val = 0
        while val == 0:
            val = randint(-35, 35)
        b[i] = val
    return bytes(b)

def interestingbytes(b: bytes) -> bytes:
    """
    Randomly replace 1 to 4 consecutive bytes with interesting values
    """
    
    b = bytearray(b)
    n = randint(1, min(4, len(b)))
    start = randint(0,  len(b) - n)

    interesting = [0, 0xFF, 1, 4, 0x7F, 0x7E]

    rand = bytearray((interesting[randint(0,len(interesting)-1)] for i in range(n)))
    b[start:] = rand
    
    return bytes(b)


def bytedelete(b: bytes) -> bytes:
    """
    Randomly delete 1 to 4 consecutive bytes
    """
    
    b = bytearray(b)
    n = randint(1, min(4, len(b)))
    start = randint(0,  len(b) - n)

    del b[start:start+n]
    
    return bytes(b)

def randominsert(b: bytes) -> bytes:
    """
    Randomly insert 1 to 4 consecutive random bytes
    """
    
    b = bytearray(b)
    n = randint(1, 4)
    start = randint(0,  len(b))

    rand = bytearray((random.getrandbits(8) for i in range(n)))
    b[start:start] = rand
    
    return bytes(b)
