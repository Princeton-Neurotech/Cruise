
import time
import numpy as np
# from threading import Timer, Thread
from pynput import keyboard
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
import tkinter as tk

def on_press(key, times):
    # aysnc key press handler
    times.append(time.time())

    # end loop if return False  --> q = quitting
    if key == 'q':
        return False
    return True

times = []
start_time = time.time()
check = False
with keyboard.Listener(on_press = lambda key: on_press(key, times)) as listener:
    while True:
        curr_time = time.time()

        if (round(curr_time - start_time) % 5) - 1 == 0 and (curr_time - start_time != 0):
            check = True
        elif (round(curr_time - start_time) % 5) == 0 and (curr_time - start_time != 0) and check == True:
            check = False
            np_times = np.array(times)
            last_ten = np_times[np.where(np_times > curr_time-10)]
            last_five = np_times[np.where(np_times > curr_time-5)]
            times = list(last_ten)

            print('Num key presses in last 10 secs', len(last_ten))
            print('Num key presses in last 5 secs', len(last_five))
