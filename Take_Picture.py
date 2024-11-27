import requests
import time

start = time.perf_counter()//2
later = start


while True:
    now = time.perf_counter()//2

    if now > later:
        print("now")
        later = start + 10
        start = now