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
    15s for past - sum up every 3 entries ie indexes 0-2, 3-5, ... for the first 60 entries
    (features are words typed in 15s intervals for past 5 mins)
    (20 groups of elements)
    60 indexes to sum for future (label = words typed in future 5mins)

    Takes 10 minutes to create datapoint 1
    after that making a new datapoint every 5s --> 60 datapoints in next 5 mins
    Therefore after 15mins have 60 datapoints

    # to make a queue
    examp_list = [1,2,3]
    examp_list.append(123) - appends 123 to the end (start of the queue)
    first_item = examp_list.pop(0) - pops start (end of the queue)
    """

    def __init__(self):
        self.PAGE_LENGTH = 4002

        self.last_charcount = 0
        self.last_wordcount = 0
        self.last_sentencecount = 0

        self.time_last_change = time.time()
        self.start_time = time.time()

        self.history_charcount = []
        self.history_word_count = []
        self.history_sentence_count = []
        self.history_page_count = []
        self.history_standby = []
        self.history_features = []
        self.name = []
        self.history_dffeatures = []

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
        print("roadblock:", self.roadblock)
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

        charcount, wordcount, sentencecount, pagecount = 0, 0, 0, 0

        dictionary = enchant.Dict("en_US")

        prompt = self.input_user_prompt.get(0.0, "end")
        completeSentences = sent_tokenize(prompt)  # produces array of sentences
        for sentence in completeSentences:
            words = word_tokenize(sentence)

            # if first letter of first word is capital, considered sentence
            if words and words[0].isupper() and dictionary.check(words[0]):
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

        print("condition:", wordcount < wordcountThresholdInt)

        pagecount = len(prompt) // self.PAGE_LENGTH
        charcount = len(prompt.replace('\n', ''))

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

        # for data collection
        self.history_page_count.append(pagecount)
        self.history_sentence_count.append(sentencecount)
        self.history_word_count.append(wordcount)
        self.history_charcount.append(charcount)
        self.history_standby.append(self.nb_standby)

        self.history_dffeatures = pd.DataFrame(self.history_features)

        self.history_dffeatures["charcount"] = self.history_charcount
        self.history_dffeatures["wordcount"] = self.history_word_count
        self.history_dffeatures["sentencecount"] = self.history_sentence_count
        self.history_dffeatures["pagecount"] = self.history_page_count
        self.history_dffeatures["standby"] = self.history_standby

        print(self.history_dffeatures)

        # put values in interface
        self.output_charcount.insert(tk.INSERT, charcount)
        self.output_wordcount.insert(tk.INSERT, wordcount)
        self.output_sentencecount.insert(tk.INSERT, sentencecount)
        self.output_pagecount.insert(tk.INSERT, pagecount)
        self.output_standby.insert(tk.INSERT, standbyNotification)

        # call realtime() every 5s
        self.main_window.after(5000, self.realtime)


if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()