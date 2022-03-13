import multiprocessing
from workers import *
import sys
import time
import brain_data_collection
import machine_learning
import brainflow

# increase recursion limit
# sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    myBoard = brain_data_collection.braindata(38, "/dev/cu.usbserial-DM03H3ZF")
    multiprocessing_ml  = machine_learning.ml()
    """
        proc1 = multiprocessing.Process(target=workers.worker1)
        proc1.start() 
        proc1.terminate()
        
    """
    # proc3 = multiprocessing.Process(target=workers.worker3)
    # proc3.daemon = True 
    # proc3.start()

    proc2 = multiprocessing.Process(target=worker2(myBoard))
    proc2.start()
    time.sleep(5)
    # myBoard.collectData(myBoard)
    # myBoard.define_global_muse_data()

    # ml process
    proc4 = multiprocessing.Process(target=worker4)
    proc4.start()
    multiprocessing_ml.process_data()
    
    proc2.terminate()
    proc4.terminate()