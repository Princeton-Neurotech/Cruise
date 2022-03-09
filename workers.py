import gui_and_keyboard_features
import brain_data_collection
import machine_learning
import web_interface
import pandas

def worker1():
    keyboard1 = only_keyboard_features.gui()
    keyboard1.getData()
    keyboard1.realtime()
 
def worker2():
    myBoard = brain_data_collection.braindata(0, '/dev/cu.usbserial-DM03H3ZF')
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