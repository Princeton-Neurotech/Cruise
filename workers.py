import gui_and_keyboard_features
import old_brain_features
import machine_learning

import time
import multiprocessing


def worker1():
    start_time = time.time()
    gui1 = gui_and_keyboard_features.gui()
    if (int(time.time() - start_time) % 5 == 0.0) and (int(time.time() - start_time) != 0):
        gui1.realtime()
    # gui1.every_5_min()
    gui1.main_window.mainloop()
 
def worker2():
    myBoard = old_brain_features.braindata(-1, 'COM3')
    myBoard.startStream()
    myBoard.collectData()
 
def worker3():
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