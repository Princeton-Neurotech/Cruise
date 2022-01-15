import time
import pandas as pd
import numpy as np
import tkinter as tk
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize

from sys import exit
import warnings
warnings.filterwarnings('ignore')

# import machine_learning

from tkinter.filedialog import asksaveasfile

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
    Last 5 minutes - 10s spacing take readings

    # Length of history list readings needed (queue) (one every 10s): 120 (past and future)
    10s for past - sliding window queue for 5s intervals with overlap (0-10, 5-15, 10-20, etc.)
    60 features - words typed in 10s intervals for past 5 mins
    1 label - 60 summed indexes for future - words typed in future 5 mins
    Can change intervals if want length of queue to be different, based on # of bins
    """
    def __init__(self):
        # 5 mins in future, 5 mins in past (length = 120, 60 and 60)
        self.wordcount = 0
        # self.ml_object = machine_learning.ml()
        self.start_time = time.time()
        self.time_last_change = time.time()
        self.PAGE_LENGTH = 4002
        self.roadblock = False
        self.nb_standby = 0
        self.wordcount_list = [0, ]
        
        self.time_for_features = time.time()
        self.history_time_seconds = []
        self.history_word_count = []
        self.history_sentence_count = []
        self.history_standby = []
        self.history_features = []
        self.history_dffeatures = []
        self.keyboard_training_features = []
        self.training_label = []

        # Root of tk popup window when opened
        self.popup_root = None

        # Main tk window
        self.main_window = tk.Tk()
        self.main_window.title("Roadblocks Project")
        self.main_window.geometry("500x600")

        """
        # saving
        self.save_root = Tk()
        self.save_root.geometry('200x150')
        """

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

        """
        saveButton = tk.Button(self.save_root, text = 'Save', command = lambda : save())
        saveButton.pack(side = TOP, pady = 20)
        """

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
        # if no popup and should have popup, display it
        if not self.popup_root:
            self.popup_root = tk.Tk()  # create popup window
            popup_button = tk.Button(self.popup_root, text="You've hit a roadblock", font=("Verdana", 12), bg="yellow", command=exit)
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

        charcount, self.wordcount, sentencecount, pagecount = 0, 0, 0, 0
        dictionary = enchant.Dict("en_US")
        prompt = self.input_user_prompt.get(0.0, "end")
        completeSentences = sent_tokenize(prompt)  # produces array of sentences
        for sentence in completeSentences:
            sentencecount += 1
            words = word_tokenize(sentence)
            for i, word in enumerate (words):
                if i == len(words) - 1:
                    if word[-1] != "." and word[-1] != "?" and word[-1] != "!":
                        sentencecount -=1
                # this dictionary counts . as words, but not ! or ?
                if dictionary.check(word) and word != ".":
                    self.wordcount += 1
        self.wordcount_list.append(self.wordcount)

        charcount = len(prompt.replace('\n', ''))
        pagecount = len(prompt) // self.PAGE_LENGTH
        
        # case: user wrote or deleted nothing for 60s
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
        if charcount == 0 or self.last_charcount != charcount:
            
            self.time_last_change = time.time()
            
        if (time.time() - self.time_last_change) > 10:
            
            standbyNotification = "You've entered a standby"
            self.history_standby.append(1)
        else:
            self.history_standby.append(0)

        # set Thresholds to -1 unless a number exists
        wordcountThresholdInt, pagecountThresholdInt = -1, -1
        try:
            wordcountThresholdInt = int(self.input_wordcount_threshold.get(0.0, "end"))
        except:
            pass
        self.last_charcount = charcount

        """
        WHEN ML MODEL IS FINISHED INCORPORATE PREDICTIONS INTO ROADBLOCK NOTIFICATION POPPING UP
        ml_label_predicted = machine_learning.training_predictions < wordcountThresholdInt
        if ml_label_predicted:
            if self.roadblock:
                self.popup_display()
            else:
                self.popup_close()
        """

        # for data collection
        self.history_word_count.append(self.wordcount)
        self.history_sentence_count.append(sentencecount)
        self.history_dffeatures = pd.DataFrame(self.history_features)
        self.history_time_seconds.append(round(time.time() - self.time_for_features, 2))
        self.history_dffeatures["time (s)"] = self.history_time_seconds

        # self.history_dffeatures["time (s)"] = self.history_time_seconds
        self.history_dffeatures["wordcount"] = self.history_word_count
        self.history_dffeatures["sentencecount"] = self.history_sentence_count
        self.history_dffeatures["standby"] = self.history_standby
        self.history_dffeatures["change in wordcount"] = self.history_dffeatures["wordcount"].diff()
        self.history_dffeatures["change in sentencecount"] = self.history_dffeatures["sentencecount"].diff()
        self.history_dffeatures["words produced"] = self.history_dffeatures["change in wordcount"].copy()
        self.history_dffeatures["words produced"][self.history_dffeatures["words produced"] < 0] = 0
        self.history_dffeatures["sentences produced"] = self.history_dffeatures["change in sentencecount"].copy()
        self.history_dffeatures["sentences produced"][self.history_dffeatures["sentences produced"] < 0] = 0
        self.history_dffeatures["words deleted"] = -1*self.history_dffeatures["change in wordcount"].copy()
        self.history_dffeatures["words deleted"][self.history_dffeatures["words deleted"] < 0] = 0
        self.history_dffeatures["words deleted"] = self.history_dffeatures["words deleted"].abs()
        self.history_dffeatures["sentences deleted"] = -1*self.history_dffeatures["change in sentencecount"].copy()
        self.history_dffeatures["sentences deleted"][self.history_dffeatures["sentences deleted"] < 0] = 0
        self.history_dffeatures["sentences deleted"] = self.history_dffeatures["sentences deleted"].abs()

        for col in self.history_dffeatures:
            if col == "wordcount" or col == "sentencecount":
                self.history_dffeatures['5rSUMMARY ' + col] = self.history_dffeatures[col].rolling(5).mean() 
            elif col == "standby":
                self.history_dffeatures["5rSUMMARY " + col] = self.history_dffeatures[col].rolling(5).max()
            elif col == "words produced" or col == "sentences produced" or col == "words deleted" or col == "sentences deleted" or col == "change in wordcount" or col == "change in sentencecount":
                self.history_dffeatures['5rSUMMARY ' + col] = self.history_dffeatures[col].rolling(5).sum() 

        # put values in interface
        self.output_charcount.insert(tk.INSERT, charcount)
        self.output_wordcount.insert(tk.INSERT, self.wordcount)
        self.output_sentencecount.insert(tk.INSERT, sentencecount)
        self.output_pagecount.insert(tk.INSERT, pagecount)
        self.output_standby.insert(tk.INSERT, standbyNotification)

        # call realtime() every ~10s
        self.main_window.after(9500, self.realtime)
    
        return self.history_dffeatures
    
    def every_5_min(self):
        # features are past data collected every 5 min
        if (int(time.time() - self.start_time) % 5 == 0.0) and (int(time.time() - self.start_time) != 0):
            self.keyboard_training_features = self.history_dffeatures[['5rSUMMARY wordcount', '5rSUMMARY sentencecount', '5rSUMMARY words produced', '5rSUMMARY sentences produced', '5rSUMMARY words deleted', '5rSUMMARY sentences deleted', '5rSUMMARY standby']]
            # print(self.keyboard_training_features) # 60 rows that will be transposed into 60 columns

        # label is sum of all future data
        self.training_label = self.history_dffeatures["words produced"][-300:].sum()
        # print(self.training_label)

        # call every_5_min() every 5 min
        self.main_window.after(300000, self.every_5_min)
    
    """
    def save():
        files = [('All Files', '*.*'), 
                ('Python Files', '*.py'),
                ('Text Document', '*.txt')]

        text = e1.get() + "\n"+e2.get() + "\n"+e3.get() 
        with open("test.txt", "w") as f:
            f.writelines(text)
        file = asksaveasfile(filetypes = files, defaultextension = files)
    """

if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()
    gui1.every_5_min()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()