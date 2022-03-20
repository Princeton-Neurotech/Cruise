import multiprocessing
from workers import *
import sys
import time
import brain_data_collection
import machine_learning
import brainflow
import pandas
from multiprocessing import Manager
# increase recursion limit
# sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    myBoard = brain_data_collection.braindata(38, "/dev/cu.usbserial-DM03H3ZF")
    #multiprocessing_ml  = machine_learning.ml()
    
    mgr = Manager()
    ns = mgr.Namespace()
    """
        proc1 = multiprocessing.Process(target=workers.worker1)
        proc1.start() 
        proc1.terminate()
        
    """
    # proc3 = multiprocessing.Process(target=workers.worker3)
    # proc3.daemon = True 
    # proc3.start()

    proc2 = multiprocessing.Process(target=worker2, args=(myBoard, ns))
    proc2.start()
    for i in range(30):
        time.sleep(5)
        print(ns)
        
    # ml process
    #proc4 = multiprocessing.Process(target=worker4)
    #proc4.start()
    #multiprocessing_ml.process_data()
    
    proc2.terminate()
    #proc4.terminate()
