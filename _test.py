import time
import random

def perf_timer(func):
    ''' 実行時間測定用デコレータ '''
    def wrapper(*args, **ky):
        start = time.perf_counter()
        random.seed(1011)
        func(*args, **ky) # <-- exec function
        end = time.perf_counter()
        print((end-start))
    return wrapper

@perf_timer
def for_loop():
    cc = 0
    for _ in iter(int, 1):
        cc += random.random()
        if cc >= 10**7:
            break
    print(f'for   :{cc}')

@perf_timer
def while_loop():
    cc = 0
    while True:
        cc += random.random()
        if cc >= 10**7:
            break
    print(f'while: {cc}')

if __name__ == "__main__":
    for_loop()
    while_loop()
