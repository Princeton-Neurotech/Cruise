import time
from typing import final
import pandas as pd
import numpy as np
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize

import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import client, file, tools

from sys import exit
import warnings
warnings.filterwarnings('ignore')

# from web_interface import entire_url
# from extract_text import *

class keyboard():
    
    def __init__(self):
        self.start_time = time.time()
        self.time_last_change = time.time()
        self.time_for_features = time.time()

        self.previous_charcount = 0
        self.PAGE_LENGTH = 4002

        self.roadblock = False

        self.nb_standby = 0
        self.wordcount_list = [0, ]
        self.features_list = ["wordcount", "sentencecount", "standby", "words produced", "sentences produced", "words deleted", "sentences deleted", "change in wordcount", "change in sentencecount"]
        self.history_time_seconds = []
        self.history_char_count = []
        self.history_word_count = []
        self.history_sentence_count = []
        self.history_standby = []
        self.history_features = []
        self.history_dffeatures = []
        
        self.row_index = 0
        self.keyboard_training_features = pd.DataFrame()
        self.training_label = []

        self.text = ''

    def realtime(self, text):
        charcount, sentencecount, pagecount = 0, 0, 0
        wordcount = 0

        dictionary = enchant.Dict("en_US")
        
        completeSentences = sent_tokenize(text)  # arg needs to be a string, produces array of sentences

        for sentence in completeSentences:
            sentencecount += 1
            words = word_tokenize(sentence)
            for i, word in enumerate (words):
                if i == len(words) - 1:
                    if word[-1] != "." and word[-1] != "?" and word[-1] != "!":
                        sentencecount -=1
                # this dictionary counts . as words, but not ! or ?
                if dictionary.check(word) and word != ".":
                    wordcount += 1
                    # self.time_last_change = time.time()
        self.wordcount_list.append(wordcount)

        # add these to csv?
        charcount = len(text.replace('\n', ''))
        if self.previous_charcount != charcount:
            self.time_last_change = time.time()
        self.previous_charcount = charcount

        pagecount = len(text) // self.PAGE_LENGTH
        
        # case: user wrote or deleted nothing for 60s
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        # standbyNotification = ""
        if (time.time() - self.time_last_change) > 10:
            #standbyNotification = "You've entered a standby"
            self.history_standby.append(1)
        else:
            self.history_standby.append(0)

        # set Thresholds to -1 unless a number exists
        # wordcountThresholdInt, pagecountThresholdInt = -1, -1
        # try:
        #    wordcountThresholdInt = int(self.input_wordcount_threshold.get(0.0, "end"))
        # except:
        #    pass
        
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
        self.history_char_count.append(charcount)
        self.history_word_count.append(wordcount)
        self.history_sentence_count.append(sentencecount)
        self.history_dffeatures = pd.DataFrame(self.history_features)
        self.history_time_seconds.append(round(time.time(), 2))
        # self.history_dffeatures["time (s)"] = self.history_time_seconds

        self.history_dffeatures["charcount"] = self.history_char_count
        self.history_dffeatures["wordcount"] = self.history_word_count
        self.history_dffeatures["sentencecount"] = self.history_sentence_count
        self.history_dffeatures["standby"] = self.history_standby
        self.history_dffeatures["change in charcount"] = self.history_dffeatures["charcount"].diff()
        self.history_dffeatures["change in wordcount"] = self.history_dffeatures["wordcount"].diff()
        self.history_dffeatures["change in sentencecount"] = self.history_dffeatures["sentencecount"].diff()
        self.history_dffeatures["chars produced"] = self.history_dffeatures["change in charcount"].copy()
        self.history_dffeatures["chars produced"][self.history_dffeatures["chars produced"] < 0] = 0
        self.history_dffeatures["words produced"] = self.history_dffeatures["change in wordcount"].copy()
        self.history_dffeatures["words produced"][self.history_dffeatures["words produced"] < 0] = 0
        self.history_dffeatures["sentences produced"] = self.history_dffeatures["change in sentencecount"].copy()
        self.history_dffeatures["sentences produced"][self.history_dffeatures["sentences produced"] < 0] = 0
        self.history_dffeatures["chars deleted"] = -1*self.history_dffeatures["change in charcount"].copy()
        self.history_dffeatures["chars deleted"][self.history_dffeatures["chars deleted"] < 0] = 0
        self.history_dffeatures["chars deleted"] = self.history_dffeatures["chars deleted"].abs()
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
            if col == "wordcount" or col == "sentencecount" or "standby":
                self.history_dffeatures['5rSUMMARY ' + col] = self.history_dffeatures[col].rolling(60, min_periods=1).mean() 
            # elif col == "standby":
            #     self.history_dffeatures["5rSUMMARY " + col] = self.history_dffeatures[col].rolling(60, min_periods=1).max()
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
        # if len(self.keyboard_training_features.index) == 1:
        #    self.keyboard_training_features.to_csv('keyboard.csv')
        
        # every 5s append one row to existing csv file to update records
        self.keyboard_training_features.loc[self.row_index - 1:self.row_index].to_csv('keyboard.csv', mode='a', header=False)

        # label is sum of all future data
        self.training_label = self.history_dffeatures["words produced"][-300:].sum()
        # print(self.training_label)

        # ml logic
        """
        notification of roadblock is prompted if roadblocks repeatedly occur for 1/6 of the inputted time
        obtain total_time variable from js like we did for doc url
        if (time.time() - self.start_time) % 300 == 0:
            saved_charcount = charcount
            saved_wordcount = wordcount
            saved_sentence_count = sentence_count

        if charcount/total_time < saved_charcount/total_time:
            take note that there could be a roadblock
        if wordcount/total_time < saved_wordcount/total_time:
            take note that there could be a roadblock
        if sentence_count/total_time < saved_sentence_count/total_time:
            take note that there could be a roadblock
        
        if standby == True:
            take note that there could be a roadblock

        if roadblock == True and (time.time() - self.start_time) > total_time/6:
            prompt notification of roadblock
        
        inputted_wordcount and inputted_pagecount taken from js
        if (wordcount == inputted_wordcount) and (pagecount = inputted_pagecount):
            prompt notification of completion of assignment
        """

        return self.keyboard_training_features
        # test both types of keyboard features in ml model and determine which has less error
        # self.keyboard_training_features # first training set - means, maxes, sums
        # return self.history_dffeatures # second training set - raw numbers

if __name__ == '__main__':
    keyboard1 = keyboard()
    # textExtractor1 = textExtractor()
    # keyboard1.realtime(textExtractor1.retrieveText(entire_url))
