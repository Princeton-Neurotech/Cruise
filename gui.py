import time
import tkinter as tk
from tkinter import *
import numpy as np
from pynput import keyboard
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
import tkinter as tk

class gui():

    def __init__(self):
        self.global_charcount = 0
        self.global_wordcount = 0
        self.global_sentencecount = 0
        self.time_last_change = time.time()
        self.start_time = time.time()
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
        if sp == 1:
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
            elif (round(time.time() - self.time_last_change, 2) > 10) and (self.start_time != 0):
                standby_notification = "You've entered a standby"

            print(self.start_time)
            self.total_sentencecount.append(sentencecount)
            self.total_wordcount.append(wordcount)
            self.total_charcount.append(charcount)

            print(round(time.time() - self.time_last_change, 2))
            self.output1.insert(tk.INSERT, charcount)
            self.output2.insert(tk.INSERT, wordcount)
            self.output3.insert(tk.INSERT, sentencecount)
            self.output4.insert(tk.INSERT, standby_notification)
            self.window.after(5000, self.realtime)

    def initUI(self):
        times = []
        # Creating interface
        self.window = tk.Tk()
        self.window.title("Count Characters")
        self.window.geometry("500x600")
        label = tk.Label(self.window, text="Input")
        # Formatting
        self.inputUser = tk.Text(self.window, width=450, height=10, font=("Helvetica", 16), wrap="word")
        self.decision = tk.IntVar()
        # Radio buttons for space counting
        r1 = tk.Radiobutton(self.window, text="Start", value=1, variable=self.decision)
        # Button to count
        button1 = tk.Button(self.window, text="Begin", command=self.realtime)
        label2 = tk.Label(self.window, text="Charcount")
        # Output Block
        self.output1 = tk.Text(self.window, width=20, height=2, font=("Helvetica", 16), wrap="word")
        label3 = tk.Label(self.window, text="Wordcount")
        self.output2 = tk.Text(self.window, width=20, height=2, font=("Helvetica", 16), wrap="word")
        label4 = tk.Label(self.window, text="Sentence count")
        self.output3 = tk.Text(self.window, width=20, height=2, font=("Helvetica", 16), wrap="word")
        label5 = tk.Label(self.window, text="Standby")
        self.output4 = tk.Text(self.window, width=20, height=2, font=("Helvetica", 16), wrap="word")

        # Function calling
        label.pack()
        self.inputUser.pack()
        r1.pack()
        label2.pack()
        self.output1.pack()
        label3.pack()
        self.output2.pack()
        label4.pack()
        self.output3.pack()
        label5.pack()
        self.output4.pack()
        button1.pack()

        self.realtime()
        self.window.mainloop()

def main():
    gui1 = gui()
    gui1.initUI()

if __name__ == '__main__':
    main()