import keyboard_features
import pandas as pd
import time
import roadblock_ml
 
# web interface functions
def worker1(mySelenium, myUID):
    while True:
        time.sleep(5)
        mySelenium.processSelenium(myUID)     
        pd.options.display.max_columns = None
        prediction = roadblock_ml.rb_ml()

 # brain data functions
def worker2(board, namespace):
    print("starting brain data collection")
    # myBoard = brain_data_collection.braindata(38, '/dev/cu.usbserial-DM03H3ZF')
    try:
        board.startStream()
    except:
        print("Stream not started")
         
    for i in range(10):
        board.collectData(board)        
        namespace.brain = board.define_global_muse_data()
        # print(namespace.brain)
    