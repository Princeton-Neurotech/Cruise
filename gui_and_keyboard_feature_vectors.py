import time
import pandas as pd
import tkinter as tk
import numpy as np
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import exit


class gui():
    """
    STANDBY:
    Discrete gui notification that you haven't typed for 60s

    ROADBLOCK:
    min_goal = 200 words / 5 minutes --> if ml predicts from brain data + recent historic
    data that not going to hit min_goal in next 5 mins tells you to stop --> we call this
    a roadblock - ml predicts 200 words / 5 minute and is trained by you typing e.g. retrain
    every 10 mins?

    CHANGES:
    Last 5 minutes - 5s spacing take readings

    # length of history list readings needed (one every 5s): 120
    5s for past - sum up every 5 entries ie indexes 0-4, 4-8, ... for the first 300 entries
    (features are words typed in 5s intervals for past 5 mins)
    (length of queue is 60) - can change to 15s intervals if want length of queue to be 20 based on # of bins
    60 indexes to sum for future (label = words typed in future 5 mins)

    Takes 10 minutes to create datapoint 1
    after that making a new datapoint every 5s --> 60 datapoints in next 5 mins
    Therefore after 15mins have 60 datapoints
    """

    def __init__(self):
        self.PAGE_LENGTH = 4002

        self.last_charcount = 0
        self.last_wordcount = 0
        self.last_sentencecount = 0

        self.time_last_change = time.time()
        self.time_for_features = time.time()
        self.history_time_seconds = []

        self.history_charcount = []
        self.history_word_count = []
        self.history_sentence_count = []
        self.history_page_count = []
        self.history_standby = []
        self.history_features = []
        self.history_dffeatures = []
        self.features_5s = 0
        self.keyboard_input_fv = []

        self.roadblock = False
        self.nb_standby = 0

        # Root of tk popup window when opened
        self.popup_root = None

        # Main tk window
        self.main_window = tk.Tk()
        self.main_window.title("Roadblocks Project")
        self.main_window.geometry("500x600")

        # Textbox for prompt
        promptLabel = tk.Label(self.main_window, text="Write prompt here")
        self.input_user_prompt = tk.Text(self.main_window, width=450, height=8, font=("Times New Roman", 12),
                                         wrap="word")

        # Textbox for wordcount threshold
        wordcountThresholdLabel = tk.Label(self.main_window, text="Wordcount threshold")
        self.input_wordcount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12),
                                                 wrap="word")

        pagecountThresholdLabel = tk.Label(self.main_window, text="Page count threshold")
        self.input_pagecount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12),
                                                 wrap="word")

        begin = tk.Button(self.main_window, text="Begin", command=self.realtime)

        charcountLabel = tk.Label(self.main_window, text="Charcount")
        self.output_charcount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        wordcountLabel = tk.Label(self.main_window, text="Wordcount")
        self.output_wordcount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        sentencecountLabel = tk.Label(self.main_window, text="Sentence count")
        self.output_sentencecount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        pagecountLabel = tk.Label(self.main_window, text="Page count")
        self.output_pagecount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        standbyLabel = tk.Label(self.main_window, text="Standby")
        self.output_standby = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        promptLabel.pack()
        self.input_user_prompt.pack()

        charcountLabel.pack()
        self.output_charcount.pack()

        wordcountLabel.pack()
        self.output_wordcount.pack()

        sentencecountLabel.pack()
        self.output_sentencecount.pack()

        pagecountLabel.pack()
        self.output_pagecount.pack()

        standbyLabel.pack()
        self.output_standby.pack()

        wordcountThresholdLabel.pack()
        self.input_wordcount_threshold.pack()

        pagecountThresholdLabel.pack()
        self.input_pagecount_threshold.pack()

        begin.pack()

    def popup_display(self):
        # print("roadblock:", self.roadblock)
        # MAKE NOTIFICATION NOT COME UP IMMEDIATELY
        # if no popup and should have popup, display it
        if not self.popup_root:
            self.popup_root = tk.Tk()  # create popup window
            popup_button = tk.Button(self.popup_root, text="You've hit a roadblock", font=("Verdana", 12), bg="yellow",
                                     command=exit)
            popup_button.pack()

    def popup_close(self):
        if self.popup_root:
            self.popup_root.destroy()  # destroys pop up window
            self.popup_root = None

    def realtime(self):
        self.output_charcount.delete(0.0, "end")
        self.output_wordcount.delete(0.0, "end")
        self.output_sentencecount.delete(0.0, "end")
        self.output_pagecount.delete(0.0, "end")
        self.output_standby.delete(0.0, "end")

        round(time.time() - self.time_for_features, 2)

        char, charcount, wordcount, sentencecount, pagecount = 0, 0, 0, 0, 0

        dictionary = enchant.Dict("en_US")

        prompt = self.input_user_prompt.get(0.0, "end")

        char = prompt.replace('\n', '')
        charcount = len(prompt.replace('\n', ''))
        pagecount = len(prompt) // self.PAGE_LENGTH

        completeSentences = sent_tokenize(prompt)  # produces array of sentences
        for sentence in completeSentences:
            words = word_tokenize(sentence)

            # if first letter of first word is capital, considered sentence
            if char[0].isupper() and dictionary.check(words[0]):
                sentencecount += 1
            for word in words:
                # this dictionary counts . as words, but not ! or ?
                if dictionary.check(word) and word != ".":
                    wordcount += 1

        # set Thresholds to -1 unless a number exists
        wordcountThresholdInt, pagecountThresholdInt = -1, -1
        try:
            wordcountThresholdInt = int(self.input_wordcount_threshold.get(0.0, "end"))
        except:
            pass
        try:
            pagecountThresholdInt = int(self.input_pagecount_threshold.get(0.0, "end"))
        except:
            pass

        # roadblock popup if haven't written enough words or pages
        self.roadblock = wordcount < wordcountThresholdInt or pagecount < pagecountThresholdInt
        if self.roadblock:
            self.popup_display()
        else:
            self.popup_close()

        # if anything has changed since last time update it and update time of last change
        if charcount != self.last_charcount or wordcount != self.last_wordcount or sentencecount != self.last_sentencecount:
            self.time_last_change = time.time()
            self.last_charcount = charcount
            self.last_wordcount = wordcount
            self.last_sentencecount = sentencecount

        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
        if time.time() - self.time_last_change > 60:
            standbyNotification = "You've entered a standby"
            self.nb_standby += 1

        # if nothing has changed from last loop and the last change was over 180s ago --> roadblock
        if time.time() - self.time_last_change > 180:
            if self.roadblock:
                self.popup_display()
            else:
                self.popup_close()

        """
        self.history_charcount.append(charcount)
        self.history_sentence_count.append(sentencecount)
        self.history_page_count.append(pagecount)
        self.history_standby.append(self.nb_standby)
        self.history_dffeatures = pd.DataFrame(self.history_features)
        """

        # for data collection
        self.history_word_count.append(wordcount)
        self.history_time_seconds.append(round(time.time() - self.time_for_features, 2))
        self.history_dffeatures = pd.DataFrame(self.history_features)
        self.history_dffeatures["time (s)"] = self.history_time_seconds
        self.history_dffeatures["wordcount"] = self.history_word_count
        self.history_dffeatures["change in wordcount"] = self.history_dffeatures["wordcount"].diff()
        self.history_dffeatures["words produced"] = self.history_dffeatures["change in wordcount"].copy()
        self.history_dffeatures["words produced"][self.history_dffeatures["words produced"] < 0] = 0
        self.history_dffeatures["words deleted"] = -1 * self.history_dffeatures["change in wordcount"].copy()
        self.history_dffeatures["words deleted"][self.history_dffeatures["words deleted"] < 0] = 0
        self.history_dffeatures["words deleted"] = self.history_dffeatures["words deleted"].abs()
        # print(self.history_dffeatures)

        """
        self.history_dffeatures["time (s)"] = self.history_time_seconds
        self.history_dffeatures["charcount"] = self.history_charcount
        self.history_dffeatures["wordcount"] = self.history_word_count
        self.history_dffeatures["sentencecount"] = self.history_sentence_count
        self.history_dffeatures["pagecount"] = self.history_page_count
        self.history_dffeatures["standby"] = self.history_standby
        self.history_dffeatures["change in charcount"] = self.history_dffeatures["charcount"].diff()
        self.history_dffeatures["change in wordcount"] = self.history_dffeatures["wordcount"].diff()
        self.history_dffeatures["change in sentencecount"] = self.history_dffeatures["sentencecount"].diff()
        self.history_dffeatures["change in pagecount"] = self.history_dffeatures["pagecount"].diff()
        self.history_dffeatures["chars produced"] = self.history_dffeatures["change in charcount"].copy()
        self.history_dffeatures["chars produced"][self.history_dffeatures["chars produced"] < 0] = 0
        self.history_dffeatures["words produced"] = self.history_dffeatures["change in wordcount"].copy()
        self.history_dffeatures["words produced"][self.history_dffeatures["words produced"] < 0] = 0
        self.history_dffeatures["sentences produced"] = self.history_dffeatures["change in sentencecount"].copy()
        self.history_dffeatures["sentences produced"][self.history_dffeatures["sentences produced"] < 0] = 0
        self.history_dffeatures["pages produced"] = self.history_dffeatures["change in pagecount"].copy()
        self.history_dffeatures["pages produced"][self.history_dffeatures["pages produced"] < 0] = 0
        self.history_dffeatures["chars deleted"] = -1*self.history_dffeatures["change in charcount"].copy()
        self.history_dffeatures["chars deleted"][self.history_dffeatures["chars deleted"] < 0] = 0
        self.history_dffeatures["chars deleted"] = self.history_dffeatures["chars deleted"].abs()
        self.history_dffeatures["words deleted"] = -1*self.history_dffeatures["change in wordcount"].copy()
        self.history_dffeatures["words deleted"][self.history_dffeatures["words deleted"] < 0] = 0
        self.history_dffeatures["words deleted"] = self.history_dffeatures["words deleted"].abs()
        self.history_dffeatures["sentences deleted"] = -1*self.history_dffeatures["change in sentencecount"].copy()
        self.history_dffeatures["sentences deleted"][self.history_dffeatures["sentences deleted"] < 0] = 0
        self.history_dffeatures["sentences deleted"] = self.history_dffeatures["sentences deleted"].abs()
        self.history_dffeatures["pages deleted"] = -1*self.history_dffeatures["change in pagecount"].copy()
        self.history_dffeatures["pages deleted"][self.history_dffeatures["pages deleted"] < 0] = 0
        self.history_dffeatures["pages deleted"] = self.history_dffeatures["pages deleted"].abs()
        """

        # collect features data, sum 5 indexes so 5s of data for first 5 min
        # if time.time() - self.time_for_features < 300:
        i = 0
        indexes = 300
        for i in range(indexes):
            # self.final_dffeatures.drop(self.final_dffeatures.columns[0], axis=1, inplace=True)
            self.features_5s = self.history_dffeatures.sum(axis=0)
            i = i + 5
            self.keyboard_input_fv = self.features_5s.tolist()
        print(self.features_5s)
        # print(self.keyboard_input_fv)

        # put values in interface
        self.output_charcount.insert(tk.INSERT, charcount)
        self.output_wordcount.insert(tk.INSERT, wordcount)
        self.output_sentencecount.insert(tk.INSERT, sentencecount)
        self.output_pagecount.insert(tk.INSERT, pagecount)
        self.output_standby.insert(tk.INSERT, standbyNotification)

        # call realtime() every 1s
        self.main_window.after(1000, self.realtime)


if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()