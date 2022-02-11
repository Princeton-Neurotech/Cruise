import time
from typing import final
import pandas as pd
import numpy as np
import tkinter as tk
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize

import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import client, file, tools

from sys import exit
import warnings
warnings.filterwarnings('ignore')

import machine_learning

class keyboard():
    
    def __init__(self):
        self.start_time = time.time()
        self.time_last_change = time.time()
        self.time_for_features = time.time()

        self.wordcount = 0
        self.PAGE_LENGTH = 4002

        self.roadblock = False

        self.nb_standby = 0
        self.wordcount_list = [0, ]
        self.features_list = ["wordcount", "sentencecount", "standby", "words produced", "sentences produced", "words deleted", "sentences deleted", "change in wordcount", "change in sentencecount"]
        self.history_time_seconds = []
        self.history_word_count = []
        self.history_sentence_count = []
        self.history_standby = []
        self.history_features = []
        self.history_dffeatures = []

        self.row_index = 0
        self.keyboard_training_features = pd.DataFrame()
        self.training_label = []
        # self.ml_object = machine_learning.ml()

        self.main_window = tk.Tk()
        self.main_window.title("Roadblocks Project")
        self.main_window.geometry("500x600")
        # need to get equivalent of this in Google Docs
        self.input_user_prompt = tk.Text(self.main_window, width=450, height=8, font=("Times New Roman", 12), wrap="word")
        self.input_user_prompt.pack()
    
    def realtime(self):
        with open('extracted.txt', 'r') as f:
            text = [line for line in f.readlines()]
            keyboard_df = pd.DataFrame(text,columns=['text'])
        charcount, self.wordcount, sentencecount, pagecount = 0, 0, 0, 0
        dictionary = enchant.Dict("en_US")
        print(type(self.elements))
        completeSentences = sent_tokenize(keyboard_df)  # arg needs to be a string, produces array of sentences
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

        charcount = len(keyboard_df.replace('\n', ''))
        pagecount = len(keyboard_df) // self.PAGE_LENGTH
        
        # case: user wrote or deleted nothing for 60s
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
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
            # WHEN ML MODEL IS FINISHED INCORPORATE PREDICTIONS INTO ROADBLOCK NOTIFICATION POPPING UP
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
        self.history_time_seconds.append(round(time.time(), 2))
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

        # SELF.HISTORY_DFFEATURES IS SECOND KEYBOARD TRAINING FEATURES
        # print(self.history_dffeatures)

        # take a rolling computation where 1st row would be computations of that row, 2nd row would be 1st and 
        # 2nd, 3rd so on until the last row, for example, is  mean of the last 60 rows
        for col in self.features_list:
            if col == "wordcount" or col == "sentencecount":
                self.history_dffeatures['5rSUMMARY ' + col] = self.history_dffeatures[col].rolling(60, min_periods=1).mean() 
            elif col == "standby":
                self.history_dffeatures["5rSUMMARY " + col] = self.history_dffeatures[col].rolling(60, min_periods=1).max()
            elif col == "words produced" or col == "sentences produced" or col == "words deleted" or col == "sentences deleted" or col == "change in wordcount" or col == "change in sentencecount":
                self.history_dffeatures['5rSUMMARY ' + col] = self.history_dffeatures[col].rolling(60, min_periods=1).sum() 
        
        # add one row of self.history_dffeature's summary columns every 5s
        # self.keyboard_training_features = self.history_dffeatures[['5rSUMMARY wordcount', '5rSUMMARY sentencecount', '5rSUMMARY words produced', '5rSUMMARY sentences produced', '5rSUMMARY words deleted', '5rSUMMARY sentences deleted', '5rSUMMARY standby']]
        # because of current rolling mean, all previous rows are NaN, need to take most current row
        self.history_dffeatures = self.history_dffeatures.tail(1)

        # concatenate rows so dataframe is continuous
        self.keyboard_training_features = pd.concat([self.keyboard_training_features, self.history_dffeatures], axis=0)
        print(self.keyboard_training_features)
        
        self.row_index += 1

        # create initial csv file for records
        if len(self.keyboard_training_features.index) == 1:
            self.keyboard_training_features.to_csv('keyboard.csv')
        
        # every 5s append one row to existing csv file to update records
        self.keyboard_training_features.loc[self.row_index - 1:self.row_index].to_csv('keyboard.csv', mode='a', header=False)

        # label is sum of all future data
        self.training_label = self.history_dffeatures["words produced"][-300:].sum()
        print(self.training_label)

        # call realtime() every 5s
        # NEED TO CALL THIS EVERY 5S WITHOUT BEING CONNECTED TO GUI
        # self.main_window.after(5000, self.realtime)

        # update and return every 5s - outputs 1 row every 5s
        return self.keyboard_training_features # first training set - means, maxes, sums
        # return self.history_dffeatures # second training set - raw numbers
        # test both types of keyboard features in ml model and determine which has less error

if __name__ == '__main__':
    keyboard1 = keyboard()
    # main processing function
    keyboard1.realtime()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    keyboard1.main_window.mainloop()