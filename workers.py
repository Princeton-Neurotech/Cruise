from only_keyboard_features import *
from brain_data_collection import *
# import web_interface
import pandas

def worker1(keyboard1):
    while True:
        keyboard1.realtime(keyboard1.text) 
 
def worker2(myBoard):
    # myBoard = brain_data_collection.braindata(38, '/dev/cu.usbserial-DM03H3ZF')
    myBoard.startStream()
    while(True):
        myBoard.collectData(myBoard)
        myBoard.define_global_muse_data()

# def worker3():
 #    myselenium = web_interface.selenium()