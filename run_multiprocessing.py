import multiprocessing
from workers import *
import matplotlib.pyplot as plt
import sys
import time
import brain_data_collection
import machine_learning
import brainflow
import pandas
from multiprocessing import Manager
from scipy.stats import linregress
# increase recursion limit
# sys.setrecursionlimit(15000)
 
if __name__ == "__main__":
    myBoard = brain_data_collection.braindata(38, "/dev/cu.usbserial-DM03H3ZF")
    keyboard1 = keyboard()
    #multiprocessing_ml  = machine_learning.ml()
    
    mgr = Manager()
    ns = mgr.Namespace()
    
    proc1 = multiprocessing.Process(target=worker1, args=(keyboard1, ns))
    proc1.start() 
    # for i in range(30):
    #    time.sleep(5)
    #    print(ns.keyboard_df)
        
    """
    proc3 = multiprocessing.Process(target=worker3)
    # proc3.daemon = True 
    proc3.start()
    for i in range(30):
      time.sleep(5)
      print(ns.keyboard_training_feaures)
    """
 
    proc2 = multiprocessing.Process(target=worker2, args=(myBoard, ns))
    proc2.start()
    brain_points = []
    keyboard_points = []
    timescale = []
    for i in range(10):
      time.sleep(5)
      brain_points.append(len(ns.brain_df))
      keyboard_points.append(len(ns.keyboard_df))
      timescale.append(5*i)
      print([len(ns.brain_df), len(ns.keyboard_df)])
    plt.plot(brain_points, timescale)
    plt.plot(keyboard_points, timescale)
    linregress(timescale, brain_points)
    linregress(timescale, keyboard_points)
    # brain_slope, brain_intercept = l
    # keyboard_slope, keyboard_intercept = 
    # print("y = " + brain_slope + "*x " + brain_intercept)
    # print("y = " + keyboard_slope + "*x " + keyboard_intercept)
    plt.show()
    # plt.legend()

    # rolling mean of 256 rows because sampling rate is 256 and getting keyboard data every 1s
    mean_brain = ns.brain_df.rolling(256, min_periods=1).mean() 
    # mean returns a pandas series, convert back to dataframe
    mean_brain_df = mean_brain.to_frame()
    print(mean_brain_df)
    # opposite dimensions, transpose
    # transposed_mean_brain_df = mean_brain_df.T

    # ml process
    # proc4 = multiprocessing.Process(target=worker4)
    # proc4.start()
    #multiprocessing_ml.process_data()
    
    proc1.terminate()
    proc2.terminate()
    #proc4.terminate()
