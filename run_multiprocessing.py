import multiprocessing
import workers
import sys
import time

# increase recursion limit
sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    # turns given process into a daemon which will run forever normally
    # subprocess is automatically terminated after the parent process ends to prevent orphan processes
    # aka kills all subprocesses
    start_time = time.time()
    proc1 = multiprocessing.Process(target=workers.worker1)
    proc1.daemon = True
    proc2 = multiprocessing.Process(target=workers.worker2)
    proc2.daemon = True 

    proc1.start() 
    proc2.start()

    if (int(time.time() - start_time)) % 15 == 0.0 and (int(time.time() - start_time)) != 0:
        proc3 = multiprocessing.Process(target=workers.worker3)
        # time.sleep(300) # do process only every 5 min
        proc3.start()
        proc3.terminate()