from Client import saveFile
from concurrent.futures import ThreadPoolExecutor
import time

if __name__ == "__main__":
    threadPool = ThreadPoolExecutor(10)
    list = []
    for i in range(1,3):
        threadPool.submit(saveFile,i)

    time.sleep(5)
