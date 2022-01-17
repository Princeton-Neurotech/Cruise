import multiprocessing
from multiprocessing import Pool
import workers
import sys
import time

# increase recursion limit
sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    """
    pool = Pool(processes = 3)
    output1 = pool.map_async(workers.worker1, [() for _ in range(1)])
    output2 = pool.map_async(workers.worker2, [() for _ in range(1)])
    output3 = pool.map_async(workers.worker3, [() for _ in range(1)])
    # print(output1)
    # print(output2)
    # print(output3)
    """

    start_time = time.time()

    # turns given process into a daemon which will run forever normally
    # subprocess is automatically terminated after the parent process ends to prevent orphan processes
    # aka kills all subprocesses
    proc1 = multiprocessing.Process(target=workers.worker1)
    # proc1.daemon = True
    proc2 = multiprocessing.Process(target=workers.worker2)
    # proc2.daemon = True
    proc3 = multiprocessing.Process(target=workers.worker3)

    proc1.start() 
    proc2.start()
    proc3.start()

    # while true creates problems
    # for i in range (0, 1000000):
        # if (int(time.time() - start_time) % 10 == 0.0) and (int(time.time() - start_time) != 0.0):
    
    # proc1.join()
    # proc2.join()
    # proc3.join()