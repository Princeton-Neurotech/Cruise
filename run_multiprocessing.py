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
    proc1 = multiprocessing.Process(target=workers.worker1)
    proc1.daemon = True
    proc2 = multiprocessing.Process(target=workers.worker2)
    proc2.daemon = True 
    proc3 = multiprocessing.Process(target=workers.worker3)
    proc3.daemon = True 

    proc1.start() 
    proc2.start()
    proc3.start()

    while True:
        proc4 = multiprocessing.Process(target=workers.worker4)
        proc4.start()
        print(self.global_muse_brain_data)
        time.sleep(300) # do process only every 5 min
        proc4.terminate()
