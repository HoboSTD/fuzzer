from random import randint, getrandbits
from sys import maxsize

def bitflip(b: bytes) -> bytes:
    """
    Invert 1 to 4 consecutive bits
    """
    
    if len(b) == 0:
        return b

    b = bytearray(b)
    n = randint(1, min(4, len(b)))
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
    
    if len(b) == 0:
        return b

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
    
    if len(b) == 0:
        return b

    b = bytearray(b)
    n = randint(1, min(4, len(b)))
    start = randint(0,  len(b) - n)

    for i in range(start, start+n):
        val = 0
        while val == 0:
            val = randint(-35, 35)
        if b[i] + val < 0:
            b[i] = 0
        elif b[i] + val > 255:
            b[i] = 255
        else:
            b[i] += val
    return bytes(b)

def interestingbytes(b: bytes) -> bytes:
    """
    Randomly replace 1 to 4 consecutive bytes with interesting values
    """
    
    if len(b) == 0:
        return b

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
    
    if len(b) == 0:
        return b

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

    rand = bytearray((getrandbits(8) for i in range(n)))
    b[start:start] = rand
    
    return bytes(b)
    
def copyinsert(b: bytes) -> bytes:
    """
    Copy 1 to n consecutive bytes and insert into a random location
    """
    
    if len(b) == 0:
        return b
    
    b = bytearray(b)
    
    n = randint(1, len(b))
    src_start = randint(0,  len(b) - n)
    copied = b[src_start:src_start+n]

    dest_start = randint(0,  len(b))
    b[dest_start:dest_start] = copied
    
    return bytes(b)
