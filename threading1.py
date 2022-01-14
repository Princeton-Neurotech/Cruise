import multiprocessing

def gui_and_keyboard_features(): 
    # import first script
    gui_and_keyboard_features()

def running_and_brain_features():
    # import second script
    running_and_brain_features()

def machine_learning():
    # import third script
    machine_learning()

if __name__ == "__main__":
    proc1 = multiprocessing.Process(target=gui_and_keyboard_features)
    proc2 = multiprocessing.Process(target=running_and_brain_features)
    proc3 = multiprocessing.Process(target=machine_learning)

    proc1.start()
    proc2.start()
    proc3.start()

    proc1.join()
    proc2.join()
    proc3.join()