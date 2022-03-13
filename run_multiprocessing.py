import multiprocessing
import workers
import sys
import time
import brain_data_collection
import brainflow

# increase recursion limit
sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    multiprocessing_brain = brain_data_collection.braindata(-1)
    process2 = True
    # daemon process will run forever normally
    # subprocess is automatically terminated after the parent process ends to prevent orphan processes
    # aka kills all subprocesses

    # keyboard - run at all times
    proc1 = multiprocessing.Process(target=workers.worker1)
    proc1.daemon = True
    # brain - only run once w issues w muse port
    if process2:
        proc2 = multiprocessing.Process(target=workers.worker2)
        process2 = False
    # google docs - run at all times
    # proc3 = multiprocessing.Process(target=workers.worker3)
    # proc3.daemon = True 

    proc1.start() 
    proc2.start()
    # proc3.start()

    while True:
        proc4 = multiprocessing.Process(target=workers.worker4)
        proc4.start()
        print(multiprocessing_brain.define_global_total_brain_data())
        time.sleep(10) # do process only every 5 min
        proc4.terminate()
