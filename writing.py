import time


def qwerty():
    start = time.perf_counter()
    q = list(x*2 for x in range(1, 1000))
    print(time.perf_counter() - start)

    return q


qwerty()