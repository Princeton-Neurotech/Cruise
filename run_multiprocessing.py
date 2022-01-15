import multiprocessing as mp
import sys
sys.setrecursionlimit(15000)

def gui_and_keyboard_features():
    # import first script
    gui_and_keyboard_features()
 
def brain_features():
    # import second script
    brain_features()
 
def machine_learning():
    # import third script
    machine_learning()
 
if __name__ == "__main__":
    proc1 = mp.Process(target=gui_and_keyboard_features)
    proc2 = mp.Process(target=brain_features)
    proc3 = mp.Process(target=machine_learning)
 
    proc1.start()
    proc2.start()
    proc3.start()
 
    proc1.join()
    proc2.join()
    proc3.join()
    
    print("finished running")