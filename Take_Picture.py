import time
import threading

def task(count):
    print("Handling task")
    time.sleep(2)
    print("task is done")


thread_1 = threading.Thread(target=task(1))
thread_2 = threading.Thread(target=task(2))




thread_1.start()
thread_2.start()

def main():


thread_1.join()
thread_2.join()