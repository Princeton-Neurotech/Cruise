import time
import tkinter as tk
from tkinter import *
import numpy as np
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import exit

class gui():

    def __init__(self):
        self.globalCharcount = 0
        self.globalWordcount = 0
        self.globalSentencecount = 0
        self.globcalPagecount = 0
        self.timeLastChange = time.time()
        self.timeRoadblock = time.time()
        self.startTime = time.time()
        self.outputCharcount = 0
        self.outputWordcount = 0
        self.outputSentencecount = 0
        self.outputPagecount = 0
        self.outputStandby = ""
        self.inputUserPrompt = 0
        self.inputUserWordcountThreshold = 0
        self.inputUserPagecountThreshold = 0
        self.window = 0
        self.popupRoot = Tk()
        self.totalCharcount = []
        self.totalWordcount = []
        self.totalSentencecount = []
        self.totalPagecount = []
        self.totalStandby = []
        self.roadblock = False
        self.popupDisplayRan = False

    def popupDisplay(self):
        self.popupRoot = Tk()
        roadblockNotification = "You've hit a roadblock"
        popupButton = Button(self.popupRoot, text=roadblockNotification, font=("Verdana", 12), bg="yellow", command=exit)
        self.popupRoot.geometry('400x50+700+500')
        popupButton.pack()
        self.popupDisplayRan = True

    def popup(self):
        print("roadblock:", self.roadblock)
        if self.roadblock and not self.popupDisplayRan:
            self.popupRoot.after(10000, self.popupDisplay)

    def quit(self):
        if not self.roadblock and self.popupDisplayRan is True:
            self.popupRoot.destroy()
            self.popupDisplayRan = False

    def realtime(self):
        self.outputCharcount.delete(0.0, "end")
        self.outputWordcount.delete(0.0, "end")
        self.outputSentencecount.delete(0.0, "end")
        self.outputPagecount.delete(0.0, "end")
        self.outputStandby.delete(0.0, "end")
        # prompt input
        prompt = self.inputUserPrompt.get(0.0, "end")
        # wordcount threshold input
        wordcountThreshold = self.inputUserWordcountThreshold.get(0.0, "end")
        # pagecount threshold input
        pagecountThreshold = self.inputUserPagecountThreshold.get(0.0, "end")
        charcount = 0
        wordcount = 0
        sentencecount = 0
        pagecount = 0
        standby_notification = ""
        localRoadblock = False
        dictionary = enchant.Dict("en_US")
        completeSentences = sent_tokenize(prompt)
        for sentence in completeSentences:
            c_wordcount = 0
            for word in word_tokenize(sentence):
                if dictionary.check(word):
                    if sentence[0] == sentence[0].upper():
                        sentencecount = sentencecount + 1
                        break
        words = word_tokenize(prompt)
        for word in words:
            if dictionary.check(word) and word != ".":
                wordcount = wordcount + 1
        wordcountThresholdInt = int('0' + wordcountThreshold)
        pagecountThresholdInt = int('0' + pagecountThreshold)
        if wordcount < wordcountThresholdInt or pagecount < pagecountThresholdInt:
            localRoadblock = True
            self.roadblock = localRoadblock
            self.popup()
        else:
            localRoadblock = False
            self.roadblock = localRoadblock
            self.quit()
            # if self.roadblock is False and self.popupDisplayRan is True and self.popupRoot.winfo_exists() is True:
                # print("exists: ", self.popupRoot.winfo_exists())
                # self.popupRoot.destroy()
        print("condition:", wordcount < wordcountThresholdInt)
        for char in prompt:
            if char == "\n":
                continue
            charcount = charcount + 1
            if charcount % 100 == 0 and charcount != 0:
                pagecount = pagecount + 1
        if charcount != self.globalCharcount or wordcount != self.globalWordcount or sentencecount != self.globalSentencecount:
            self.time_last_change = time.time()
            self.globalCharcount = charcount
            self.globalWordcount = wordcount
            self.globalSentencecount = sentencecount
        elif (round(time.time() - self.timeLastChange, 2) > 60) and (self.startTime != 0):
            standbyNotification = "You've entered a standby"
        if (round(time.time() - self.timeLastChange, 2) > 180) and (self.startTime != 0):
            localRoadblock = True
            self.roadblock = localRoadblock
            self.popup()
        else:
            self.roadblock = False

        self.totalPagecount.append(pagecount)
        self.totalSentencecount.append(sentencecount)
        self.totalWordcount.append(wordcount)
        self.totalCharcount.append(charcount)
        self.totalStandby.append(self.totalStandby.count("You've entered a standby"))

        # print(round(time.time() - self.time_last_change, 2))
        self.outputCharcount.insert(tk.INSERT, charcount)
        self.outputWordcount.insert(tk.INSERT, wordcount)
        self.outputSentencecount.insert(tk.INSERT, sentencecount)
        self.outputPagecount.insert(tk.INSERT, pagecount)
        self.outputStandby.insert(tk.INSERT, standby_notification)

        # repeatedly call realtime()
        self.window.after(5000, self.realtime)

    def initUI(self):
        times = []
        # Create interface
        self.window = tk.Tk()
        self.window.title("Roadblocks Project")
        self.window.geometry("500x600")

        # Textbox for prompt
        promptLabel = tk.Label(self.window, text="Write prompt here")
        self.inputUserPrompt = tk.Text(self.window, width=450, height=8, font=("Times New Roman", 12), wrap="word")

        # Textbox for wordcount threshold
        wordcountThresholdLabel = tk.Label(self.window, text="Wordcount threshold")
        self.inputUserWordcountThreshold = tk.Text(self.window, width=10, height=1, font=("Helvetica", 12), wrap="word")

        pagecountThresholdLabel = tk.Label(self.window, text="Page count threshold")
        self.inputUserPagecountThreshold = tk.Text(self.window, width=10, height=1, font=("Helvetica", 12), wrap="word")

        begin = tk.Button(self.window, text="Begin", command=self.realtime)

        charcountLabel = tk.Label(self.window, text="Charcount")
        self.outputCharcount = tk.Text(self.window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        wordcountLabel = tk.Label(self.window, text="Wordcount")
        self.outputWordcount = tk.Text(self.window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        sentencecountLabel = tk.Label(self.window, text="Sentence count")
        self.outputSentencecount = tk.Text(self.window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        pagecountLabel = tk.Label(self.window, text="Page count")
        self.outputPagecount = tk.Text(self.window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        standbyLabel = tk.Label(self.window, text="Standby")
        self.outputStandby = tk.Text(self.window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        promptLabel.pack()
        self.inputUserPrompt.pack()

        charcountLabel.pack()
        self.outputCharcount.pack()

        wordcountLabel.pack()
        self.outputWordcount.pack()

        sentencecountLabel.pack()
        self.outputSentencecount.pack()

        pagecountLabel.pack()
        self.outputPagecount.pack()

        standbyLabel.pack()
        self.outputStandby.pack()

        wordcountThresholdLabel.pack()
        self.inputUserWordcountThreshold.pack()

        pagecountThresholdLabel.pack()
        self.inputUserPagecountThreshold.pack()

        begin.pack()

        self.popup()
        self.realtime()
        self.window.mainloop()
        self.popupRoot.mainloop()

def main():
    gui1 = gui()
    gui1.initUI()

if __name__ == '__main__':
    main()