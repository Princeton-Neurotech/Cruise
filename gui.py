import time
import tkinter as tk
from tkinter import *
import numpy as np
from pynput import keyboard
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
import tkinter as tk

def key_press(key, times):
    # asynchronous key press handler
    times.append(time.time())

    # end loop if return False --> q = quitting
    # what if user presses q key?
    if key == 'q':
        return False
    return True

times = []
start_time = time.time()
check = False

def realtime_charcount():
    output1.delete(0.0, "end")
    output2.delete(0.0, "end")
    output3.delete(0.0, "end")
    # input from user
    w = inputUser.get(0.0, "end")
    print(w)
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
    # elif sp == 3:

def realtime():
    output1.delete(0.0, "end")
    output2.delete(0.0, "end")
    output3.delete(0.0, "end")
    # input from user
    w = inputUser.get(0.0, "end")
    # decision of whether you count spaces
    sp = decision.get()
    # count of chars
    charcount = 0
    wordcount = 0
    sentencecount = 0
    # settings for spaces or without spaces
    if sp == 3:
        dictionary = enchant.Dict("en_US")
        complete_sentences = sent_tokenize(w)
        print(complete_sentences)
        for sentence in complete_sentences:
            c_wordcount = 0
            for word in word_tokenize(sentence):
                if dictionary.check(word):
                    if sentence[0] == sentence[0].upper():
                        sentencecount = sentencecount + 1
                        break
        words = word_tokenize(w)
        for word in words:
            if dictionary.check(word):
                wordcount = wordcount + 1
        # print(words, wordcount)
        for k in w:
            if k == "\n":
                continue
            charcount = charcount + 1

        output1.insert(tk.INSERT, charcount)
        output2.insert(tk.INSERT, wordcount)
        output3.insert(tk.INSERT, sentencecount)
        window.after(5000, realtime)

    # output1.insert(tk.INSERT, count)

with keyboard.Listener(on_press=lambda key: key_press(key, times)) as listener:

    # Creating interface
    window = tk.Tk()
    window.title("Count Characters")
    window.geometry("500x600")
    label = tk.Label(window, text = "Input")
    # Formatting
    inputUser = tk.Text(window, width=450, height=10, font=("Helvetica", 16), wrap="word")
    decision = tk.IntVar()
    # Radio buttons for space counting
    r1 = tk.Radiobutton(window, text="with spaces", value=1, variable=decision)
    r2 = tk.Radiobutton(window, text="without spaces", value=2, variable=decision)
    r3 = tk.Radiobutton(window, text="realtime", value=3, variable=decision)
    # Button to count
    button = tk.Button(window, text="Count the number of characters", command=realtime)
    label2 = tk.Label(window, text="number of characters")
    # Output Block
    output1 = tk.Text(window, width=20, height=2, font=("Helvetica", 16), wrap="word")
    output2 = tk.Text(window, width=20, height=2, font=("Helvetica", 16), wrap="word")
    output3 = tk.Text(window, width=20, height=2, font=("Helvetica", 16), wrap="word")

    # Function calling
    label.pack()
    inputUser.pack()
    r1.pack()
    r2.pack()
    r3.pack()
    label2.pack()
    output1.pack()
    output2.pack()
    output3.pack()
    button.pack()

    realtime()
    window.mainloop()