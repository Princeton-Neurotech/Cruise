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
    myml = machine_learning.ml()
    myml.read_csv()
    # myml.add_training_data()
    # myml.train_model()
    # myml.predict()