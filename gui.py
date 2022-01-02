import time
import tkinter as tk
from tkinter import *
import numpy as np
from pynput import keyboard

def key_press(key, times):
    # asynchronous key press handler
    times.append(time.time())

    # end loop if return False --> q = quitting
    # what if user presses q key?
    if key == 'q':
        return False
    return True

def realtime_charcount():
    output1.delete(0.0, "end")
    output2.delete(0.0, "end")
    output3.delete(0.0, "end")
    # input from user
    w = inputUser.get(0.0, "end")
    # decision of whether you count spaces
    sp = decision.get()
    # count of chars
    count = 0
    # number of key presses in last 10 sec
    last_ten = 0
    # number of key presses in last 5 sec
    last_five = 0
# settings for spaces or without spaces
    if sp == 1:
        for k in w:
            if k == "\n":
                continue
            count = count + 1
    elif sp == 2:
        for k in w:
            if k == " " or k == "\n":
                continue
            count = count + 1

# def realtime_charcount():
    times = []
    start_time = time.time()
    check = False
    with keyboard.Listener(on_press=lambda key: key_press(key, times)) as listener:
        # while True:
        curr_time = time.time()

        for i in w:
            i = ((round(curr_time - start_time) % 5) - 1 == 0 and (curr_time - start_time != 0))
            if i == TRUE:
                check = True
            elif (round(curr_time - start_time) % 5) == 0 and (curr_time - start_time != 0) and check == True:
                check = False
                np_times = np.array(times)
                last_ten = np_times[np.where(np_times > curr_time-10)]
                last_five = np_times[np.where(np_times > curr_time-5)]
                times = list(last_ten)

                master = Tk()
                output_last_ten = IntVar(master, name="output_last_ten")
                master.setvar(name="output_last_ten", value=last_ten)
                print("Value of IntVar()", master.getvar(name="output_last_ten"))

                master = Tk()
                output_last_five = IntVar(master, name="output_last_five")
                master.setvar(name="output_last_five", value=last_five)
                print("Value of IntVar()", master.getvar(name="output_last_five"))

    output1.insert(tk.INSERT, count)
    output2.insert(tk.INSERT, last_ten)
    output3.insert(tk.INSERT, last_five)

# Creating interface
window = tk.Tk()
window.title("Count Characters")
window.geometry("500x600")
label = tk.Label(window, text = "Input")
# Formatting
inputUser = tk.Text(window, width=450, height=10, font=("Helvetica", 16), wrap="word")
decision=tk.IntVar()
# Radio buttons for space counting
r1 = tk.Radiobutton(window, text="with spaces", value=1, variable=decision)
r2 = tk.Radiobutton(window, text="without spaces", value=2, variable=decision)
# Button to count
button = tk.Button(window, text="Count the number of characters", command=realtime_charcount)
label2 = tk.Label(window, text="number of characters")
# Output Block
output1 = tk.Text(window,width=20, height=2, font=("Helvetica", 16), wrap="word")
output2 = tk.Text(window, width=20, height=2, font=("Helvetica", 16), wrap="word")
output3 = tk.Text(window, width=20, height=2, font=("Helvetica", 16), wrap="word")

# Function calling
label.pack()
inputUser.pack()
r1.pack()
r2.pack()
label2.pack()
output1.pack()
output2.pack()
output3.pack()
button.pack()

window.mainloop()