import time
import tkinter as tk
import numpy as np
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import exit

class gui():

    def __init__(self):
        self.PAGE_LENGTH = 4002

        self.globalCharcount = 0
        self.globalWordcount = 0
        self.globalSentencecount = 0
        self.globcalPagecount = 0

        self.timeLastChange = time.time()
        self.timeRoadblock = time.time()
        self.startTime = time.time()

        self.popupRoot = None

        self.totalCharcount = []
        self.totalWordcount = []
        self.totalSentencecount = []
        self.totalPagecount = []
        self.totalStandby = []

        self.roadblock = False
        self.nb_standby = 0

        # Create interface
        self.main_window = tk.Tk()
        self.main_window.title("Roadblocks Project")
        self.main_window.geometry("500x600")

        # Textbox for prompt
        promptLabel = tk.Label(self.main_window, text="Write prompt here")
        self.inputUserPrompt = tk.Text(self.main_window, width=450, height=8, font=("Times New Roman", 12), wrap="word")

        # Textbox for wordcount threshold
        wordcountThresholdLabel = tk.Label(self.main_window, text="Wordcount threshold")
        self.inputUserWordcountThreshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12), wrap="word")

        pagecountThresholdLabel = tk.Label(self.main_window, text="Page count threshold")
        self.inputUserPagecountThreshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12), wrap="word")

        begin = tk.Button(self.main_window, text="Begin", command=self.realtime)

        charcountLabel = tk.Label(self.main_window, text="Charcount")
        self.outputCharcount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        wordcountLabel = tk.Label(self.main_window, text="Wordcount")
        self.outputWordcount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        sentencecountLabel = tk.Label(self.main_window, text="Sentence count")
        self.outputSentencecount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        pagecountLabel = tk.Label(self.main_window, text="Page count")
        self.outputPagecount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        standbyLabel = tk.Label(self.main_window, text="Standby")
        self.outputStandby = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

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

    def popupDisplay(self):
        print("roadblock:", self.roadblock)
        # MAKE NOTIFICATION NOT COME UP IMMEDIATELY
        # if no popup and should have popup, display it
        if not self.popupRoot:
            self.popupRoot = tk.Tk() # create popup window
            popupButton = tk.Button(self.popupRoot, text="You've hit a roadblock", font=("Verdana", 12), bg="yellow", command=exit)
            popupButton.pack()

    def popupClose(self):
        if self.popupRoot:
            self.popupRoot.destroy() # destroys pop up window
            self.popupRoot = None

    def realtime(self):
        self.outputCharcount.delete(0.0, "end")
        self.outputWordcount.delete(0.0, "end")
        self.outputSentencecount.delete(0.0, "end")
        self.outputPagecount.delete(0.0, "end")
        self.outputStandby.delete(0.0, "end")
        
        charcount, wordcount, sentencecount, pagecount = 0, 0, 0, 0
        
        dictionary = enchant.Dict("en_US")

        prompt = self.inputUserPrompt.get(0.0, "end")
        completeSentences = sent_tokenize(prompt) # produces array of sentences
        for sentence in completeSentences:
            words = word_tokenize(sentence)

            # if first letter of first word is capital, considered sentence
            if words and words[0].isupper() and dictionary.check(words[0]):
                sentencecount+=1
            for word in words:
                # this dictionary counts . as words, but not ! or ?
                if dictionary.check(word) and word != ".":
                    wordcount += 1

        # set Thresholds to -1 unless a number exists
        wordcountThresholdInt, pagecountThresholdInt = -1, -1
        try: wordcountThresholdInt = int(self.inputUserWordcountThreshold.get(0.0, "end"))
        except: pass
        try: pagecountThresholdInt = int(self.inputUserPagecountThreshold.get(0.0, "end"))
        except: pass

        # roadblock popup if haven't written enough words or pages
        self.roadblock = wordcount < wordcountThresholdInt or pagecount < pagecountThresholdInt
        if self.roadblock:
            self.popupDisplay()
        else:
            self.popupClose()

        print("condition:", wordcount < wordcountThresholdInt)
        
        pagecount = len(prompt) // self.PAGE_LENGTH
        charcount = len(prompt.replace('\n',''))

        # if anything has changed since last time update it and update time of last change
        if charcount != self.globalCharcount or wordcount != self.globalWordcount or sentencecount != self.globalSentencecount:
            self.timeLastChange = time.time()
            self.globalCharcount = charcount
            self.globalWordcount = wordcount
            self.globalSentencecount = sentencecount
        
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
        if time.time() - self.timeLastChange > 60:
            standbyNotification = "You've entered a standby"
            self.nb_standby += 1

        # if nothing has changed from last loop and the last change was over 180s ago --> roadblock
        if time.time() - self.timeLastChange > 180:
            if self.roadblock:
                self.popupDisplay()
            else:
                self.popupClose()

        # for data collection
        self.totalPagecount.append(pagecount)
        self.totalSentencecount.append(sentencecount)
        self.totalWordcount.append(wordcount)
        self.totalCharcount.append(charcount)
        self.totalStandby.append(self.nb_standby)

        # put values in interface
        self.outputCharcount.insert(tk.INSERT, charcount)
        self.outputWordcount.insert(tk.INSERT, wordcount)
        self.outputSentencecount.insert(tk.INSERT, sentencecount)
        self.outputPagecount.insert(tk.INSERT, pagecount)
        self.outputStandby.insert(tk.INSERT, standbyNotification)

        # call realtime() every 5s
        self.main_window.after(5000, self.realtime)

if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()