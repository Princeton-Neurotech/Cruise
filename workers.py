import gui_and_keyboard_features
import old_brain_features
import machine_learning
import pandas as pd 
import time
import multiprocessing


df_5sec = pd.DataFrame()
def worker1(tk_object):
    gui1 = gui_and_keyboard_features.gui()
    df_5sec = gui1.realtime()
    gui1.main_window.mainloop()
 
def worker2(tk_object):
    myBoard = old_brain_features.braindata(-1, 'COM3', df_5sec)
    myBoard.startStream()
    myBoard.collectData()
 
def worker3(tk_object):
    myml = machine_learning.ml()
    myml.read_csv()
    # myml.add_training_data()
    # myml.train_model()
    # myml.predict()

# turns given process into a daemon which will run forever normally
# subprocess is automatically terminated after the parent process ends to prevent orphan processes
# aka kills all subprocesses
"""
def process1():
    proc1 = multiprocessing.Process(target=worker1)
    proc1.daemon = True
    proc1.start() 

def process2():
    proc2 = multiprocessing.Process(target=worker2)
    proc2.daemon = True
    proc2.start()

def process3():
    proc3 = multiprocessing.Process(target=worker3)
    proc3.daemon = True
    proc3.start()
"""