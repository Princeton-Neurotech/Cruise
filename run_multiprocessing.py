import multiprocessing
from multiprocessing import Pool
import workers
import sys
import time

# increase recursion limit
sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    # turns given process into a daemon which will run forever normally
    # subprocess is automatically terminated after the parent process ends to prevent orphan processes
    # aka kills all subprocesses
    proc1 = multiprocessing.Process(target=workers.worker1)
    proc1.daemon = True
    proc2 = multiprocessing.Process(target=workers.worker2)
    proc2.daemon = True
    proc3 = multiprocessing.Process(target=workers.worker3)
    proc3.daemon = True

    proc1.start() 
    proc2.start()
    
    for i in range (0, 1000000):
        time.sleep(310)
        proc3.start()
        proc3.join()
        # proc3.terminate()
        
    # while True creates problems
    
    proc1.join()
    proc2.join()
    proc3.join()

    print("finished running")