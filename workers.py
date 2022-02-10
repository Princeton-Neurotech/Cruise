import gui_and_keyboard_features
import final_brain_features
import machine_learning
import web_interface
import pandas

def worker1():
    gui1 = gui_and_keyboard_features.gui()
    gui1.realtime()
    gui1.flickering_screen()
    gui1.main_window.mainloop()
 
def worker2():
    myBoard = final_brain_features.braindata(0, '/dev/cu.usbserial-DM03H3ZF')
    myBoard.startStream()
    myBoard.collectData()

def worker3():
    myselenium = web_interface.selenium()
 
def worker4():
    myml = machine_learning.ml()
    myml.read_csv()
    # myml.add_training_data()
    # myml.train_model()
    # myml.predict()