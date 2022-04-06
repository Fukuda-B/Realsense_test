import time

start = time.perf_counter()
cc = 0
for _ in [None]:
    cc += 1
    if cc >= 10**8:
        break
end = time.perf_counter()
print((end-start))

start = time.perf_counter()
cc = 0
while True:
    cc += 1
    if cc >= 10**8:
        break
end = time.perf_counter()
print((end - start))

# output:
#
# > py .\_test.py
# 2.300000000010627e-06
# 11.7496645
