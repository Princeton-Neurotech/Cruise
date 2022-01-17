import gui_and_keyboard_features
import brain_features
import machine_learning
import time

def worker1():
    gui1 = gui_and_keyboard_features.gui()
    gui1.realtime()
    gui1.every_5_min()
    gui1.main_window.mainloop()
 
def worker2():
    myBoard = brain_features.braindata(-1, 'COM3')
    myBoard.startStream()
    myBoard.collectData()
 
def worker3():
    # machine learning related
    myml = machine_learning.ml()
    # myml.add_raw_data()
    # needed every 5 min
    time.sleep(10)
    # myml.add_training_data()
    # myml.train_model()
    # myml.predict()
    # keyboard related
    # ml_keyboard_data = gui_and_keyboard_features.gui()
    # ml_keyboard_data.realtime()
    # ml_keyboard_data.every_5_min()
    # ml_keyboard_data.main_window.mainloop()
    # brain related
    # ml_brain_data = brain_features.braindata()
    # ml_brain_data.startStream()
    # ml_brain_data.collectData()