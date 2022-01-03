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

class gui():

    def __init__(self):
        self.global_charcount = 0
        self.global_wordcount = 0
        self.global_sentencecount = 0
        self.time_last_change = 0
        self.start_time = time.time()
        self.check = False
        self.output1 = 0
        self.output2 = 0
        self.output3 = 0
        self.output4 = 0
        self.inputUser = 0
        self.decision = 0
        self.window = 0
        self.total_charcount = []
        self.total_wordcount = []
        self.total_sentencecount = []
        self.total_standby = []

    def realtime_charcount(self):
        self.output1.delete(0.0, "end")
        self.output2.delete(0.0, "end")
        self.output3.delete(0.0, "end")
        # input from user
        w = self.inputUser.get(0.0, "end")
        print(w)
        # decision of whether you count spaces
        sp = self.decision.get()
        # count of chars
        count = 0
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

    def realtime(self):
        self.output1.delete(0.0, "end")
        self.output2.delete(0.0, "end")
        self.output3.delete(0.0, "end")
        self.output4.delete(0.0, "end")
        # input from user
        w = self.inputUser.get(0.0, "end")
        # decision of whether you count spaces
        sp = self.decision.get()
        # count of chars
        charcount = 0
        wordcount = 0
        sentencecount = 0
        standby_notification = ""
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
            for k in w:
                if k == "\n":
                    continue
                charcount = charcount + 1
            if charcount != self.global_charcount or wordcount != self.global_wordcount or sentencecount != self.global_sentencecount:
                self.time_last_change = time.time()
                self.global_charcount = charcount
                self.global_wordcount = wordcount
                self.global_sentencecount = sentencecount
            elif (round(time.time() - self.time_last_change, 2) > 10):
                standby_notification = "You've entered a standby"

            self.total_sentencecount = self.total_sentencecount.append(sentencecount)


            print(round(time.time() - self.time_last_change, 2))
            self.output1.insert(tk.INSERT, charcount)
            self.output2.insert(tk.INSERT, wordcount)
            self.output3.insert(tk.INSERT, sentencecount)
            self.output4.insert(tk.INSERT, standby_notification)
            self.window.after(5000, self.realtime)

if __name__ == '__main__':
    gui1 = gui()
    times = []
    with keyboard.Listener(on_press=lambda key: key_press(key, times)) as listener:

        # Creating interface
        gui1.window = tk.Tk()
        gui1.window.title("Count Characters")
        gui1.window.geometry("500x600")
        label = tk.Label(gui1.window, text="Input")
        # Formatting
        gui1.inputUser = tk.Text(gui1.window, width=450, height=10, font=("Helvetica", 16), wrap="word")
        gui1.decision = tk.IntVar()
        # Radio buttons for space counting
        r1 = tk.Radiobutton(gui1.window, text="with spaces", value=1, variable=gui1.decision)
        r2 = tk.Radiobutton(gui1.window, text="without spaces", value=2, variable=gui1.decision)
        r3 = tk.Radiobutton(gui1.window, text="realtime", value=3, variable=gui1.decision)
        # Button to count
        button1 = tk.Button(gui1.window, text="Count the number of characters", command=gui1.realtime)
        label2 = tk.Label(gui1.window, text="number of characters")
        # Output Block
        gui1.output1 = tk.Text(gui1.window, width=20, height=2, font=("Helvetica", 16), wrap="word")
        gui1.output2 = tk.Text(gui1.window, width=20, height=2, font=("Helvetica", 16), wrap="word")
        gui1.output3 = tk.Text(gui1.window, width=20, height=2, font=("Helvetica", 16), wrap="word")
        gui1.output4 = tk.Text(gui1.window, width=20, height=2, font=("Helvetica", 16), wrap="word")

        # Function calling
        label.pack()
        gui1.inputUser.pack()
        r1.pack()
        r2.pack()
        r3.pack()
        label2.pack()
        gui1.output1.pack()
        gui1.output2.pack()
        gui1.output3.pack()
        gui1.output4.pack()
        button1.pack()

        gui1.realtime()
        gui1.window.mainloop()