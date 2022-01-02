import time
import numpy as np
# from threading import Timer, Thread
from pynput import keyboard
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
import tkinter as tk

print("Press ENTER to start the stopwatch")
print("and, press CTRL + C to stop the stopwatch")

class MyException(Exception): pass

def on_press(key, times):
    # aysnc key press handler
    times.append(time.time())

    # end loop if return False  --> q = quitting
    if key=='q':
        return False
    return True

    dict = enchant.Dict("en_US")

    char_list = ""
    correctly_spelled = ""
    complete_sentence = ""
    while True:
        if key == keyboard.Key.esc:
            raise MyException(key)
        try:
            alphanumeric_key = "{0}".format(key.char)
            print("key pressed: ", alphanumeric_key)
            char_list += alphanumeric_key
        except AttributeError:
            special_key = "{0}".format(key)
            print("key pressed: ", special_key)
            char_list += special_key

        print(char_list)
        # separate characters based on spaces
        words = word_tokenize(char_list)
        print(words)
        if dict.check(words[len(words) - 1]):
            correctly_spelled += words[len(words) - 1]
            print("correctly spelled words: ", correctly_spelled)
            print(len(correctly_spelled))
            complete_sentence = sent_tokenize(correctly_spelled)
            period = "."
            if period in correctly_spelled:
                complete_sentence.append(correctly_spelled)
                print("complete sentences: ", complete_sentence)

        charcount = len(char_list)
        print("charcount: ", charcount)

        wordcount = len(correctly_spelled)
        print("wordcount: ", wordcount)

        sentence_count = len(complete_sentence)
        print("sentence count: ", sentence_count)

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