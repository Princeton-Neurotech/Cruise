import multiprocessing
from multiprocessing import Pool
import workers
import sys
import time
# import schedule

# increase recursion limit
sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    """"
    schedule.every(.001).seconds.do(workers.process1, workers.worker1)
    schedule.every(.001).seconds.do(workers.process2, workers.worker2)
    schedule.every(310).seconds.do(workers.process3, workers.worker3)

    while 1:
        schedule.run_pending()
    """

    # turns given process into a daemon which will run forever normally
    # subprocess is automatically terminated after the parent process ends to prevent orphan processes
    # aka kills all subprocesses
    proc1 = multiprocessing.Process(target=workers.worker1)
    proc1.daemon = True
    proc2 = multiprocessing.Process(target=workers.worker2)
    proc2.daemon = True 

    proc1.start() 
    proc2.start()

    while True:
        proc3 = multiprocessing.Process(target=workers.worker3)
        time.sleep(310)
        proc3.start()
        proc3.join()
        proc3.terminate()