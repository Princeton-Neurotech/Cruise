import time
import numpy as np
# from threading import Timer, Thread
from pynput import keyboard
import enchant
from nltk.tokenize import word_tokenize
import tkinter as tk

print("Press ENTER to start the stopwatch")
print("and, press CTRL + C to stop the stopwatch")

class MyException(Exception): pass

def on_press(key, times):
    # aysnc key press handler
    times.append(time.time())

    dict = enchant.Dict("en_US")

    while True:
        char_list = []
        if key == keyboard.Key.esc:
            raise MyException(key)
        try:
            alphanumeric_key = "{0}".format(key.char)
            print("key pressed: ", alphanumeric_key)
            char_list.append(alphanumeric_key)
        except AttributeError:
            special_key = "{0}".format(key)
            print("key pressed: ", special_key)
            char_list.append(special_key)

        print(char_list)
        # separate characters based on spaces
        words = word_tokenize(alphanumeric_key)
        print(words)
        correctly_spelled = []
        if dict.check(words[0]):
            correctly_spelled.append(words)
            print("correctly spelled words: ", correctly_spelled)

            complete_sentence = []
            if correctly_spelled:
                index = len(correctly_spelled) - 1
                if correctly_spelled[index] == input("."):
                    complete_sentence.append(correctly_spelled)
                    print("complete sentences: ", complete_sentence)

        charcount = len(char_list)
        print("charcount: ", charcount)

        wordcount = len(correctly_spelled)
        print("wordcount: ", wordcount)

        sentence_count = len(complete_sentence)
        print("sentence count: ", sentence_count)

    # end loop if return False  --> q = quitting
    if key=='q':
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

def realtime_charcount():
    output.delete(0.0,"end")
    w=inputUser.get(0.0,"end")
    sp=decision.get()
    c=0
#specifying conditions
    if sp==1:
        for k in w:
            if k=="\n":
                continue
            c=c+1
    elif sp==2:
        for k in w:
            if k==" " or k=="\n":
                continue
            c=c+1

    output.insert(tk.INSERT,c)
#creating interface
window=tk.Tk()
window.title("Count Characters")
window.geometry("500x600")
label=tk.Label(window,text="Input")
#Formatting
inputUser=tk.Text(window,width=450,height=10,font=("Helvetica",16),wrap="word")
decision=tk.IntVar()
#Radio buttons for space counting
r1=tk.Radiobutton(window,text="with spaces",value=1,variable=decision)
r2=tk.Radiobutton(window,text="without spaces",value=2,variable=decision)
#BUtton to count
button=tk.Button(window,text="Count the number of characters",command=realtime_charcount)
label2=tk.Label(window,text="number of characters")
#Output Block
output=tk.Text(window,width=20,height=2,font=("Helvetica",16),wrap="word")

#Function calling
label.pack()
inputUser.pack()
r1.pack()
r2.pack()
label2.pack()
output.pack()
button.pack()

window.mainloop()