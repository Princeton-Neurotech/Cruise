import gui_and_keyboard_features
import brain_features
import machine_learning

import multiprocessing as mp
import sys
import time

# increase recursion limit
sys.setrecursionlimit(15000)

def first_file():
    gui1 = gui_and_keyboard_features.gui()
    gui1.realtime()
    gui1.every_5_min()
    gui1.main_window.mainloop()
 
def second_file():
    myBoard = brain_features.braindata(-1, 'COM3')
    myBoard.startStream()
    myBoard.collectData()
    # print(myBoard.compressed_brain_training_features)
 
def third_file():
    myml = machine_learning.ml()
    myml.add_raw_data()
    ml_keyboard_data = gui_and_keyboard_features.gui()
    ml_keyboard_data.realtime()
    ml_keyboard_data.every_5_min()
    ml_keyboard_data.main_window.mainloop()
    ml_brain_data = brain_features.braindata()
    ml_brain_data.startStream()
    ml_brain_data.collectData()
    # myml.add_training_data()
    # myml.train_model()
    # myml.predict()
 
if __name__ == "__main__":
    start_time = time.time()

    proc1 = mp.Process(target=first_file)
    proc2 = mp.Process(target=second_file)
    proc3 = mp.Process(target=third_file)

    proc1.start()
    proc2.start()
    # proc3.start()
    proc1.join()
    proc2.join()
    # proc3.join()
 
    if (int(time.time() - start_time) % 10 == 0) and (int(time.time() - start_time) != 0):
        proc3.start()
        proc3.join()
    
    print("finished running")