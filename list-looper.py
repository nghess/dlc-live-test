import numpy as np



def list_looper(i, chunk, list):
    neg = i-chunk-1
    stub = list[i-1::-1] + list[:neg:-1]
    return stub


seq = [x for x in range(1, 256)]
i = 0

while True:
    i += 1
    stub = list_looper(i, 10, seq)
    print(stub)
    if i == 10:
        i = 0
