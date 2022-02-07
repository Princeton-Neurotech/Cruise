import time
from typing import final
import pandas as pd
import numpy as np
import tkinter as tk
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize

from sys import exit
import warnings
warnings.filterwarnings('ignore')

import machine_learning

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
        self.start_time = time.time()
        self.time_last_change = time.time()
        self.time_for_features = time.time()

        self.wordcount = 0
        self.PAGE_LENGTH = 4002

        self.roadblock = False
        self.is_white = False

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

        # Root of tk popup window when opened
        self.popup_root = None

        # Main tk window
        self.main_window = tk.Tk()
        self.main_window.title("Roadblocks Project")
        self.main_window.geometry("500x600")

        promptLabel = tk.Label(self.main_window, text="Write prompt here")
        # how to pass self into canvas without passing too many arguments?
        # self.canvas = tk.Canvas(self.main_window, 450, 8)
        self.input_user_prompt = tk.Text(self.main_window, width=450, height=8, font=("Times New Roman", 12), wrap="word")

        # Textbox for wordcount threshold
        wordcountThresholdLabel = tk.Label(self.main_window, text="Wordcount threshold")
        self.input_wordcount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12), wrap="word")

        pagecountThresholdLabel = tk.Label(self.main_window, text="Page count threshold")
        self.input_pagecount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12), wrap="word")

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
    
    # can't access pixels or overlay with text widget object, so make a canvas (above) and make rectangles
    # to overlay, changing these rectangles' colors randomly
   #  def flickering_screen(self):
        # # for every pixel in textbox, switch between red and white, inducing flickering effect
        # canvas = tk.Canvas(self.main_window, 450, 8)
        # # create a matrix of dimensions of textbox filled with random values between 0 and 1
        # random_pixels = np.random.rand(450, 8)
        # # for i in random_pixels.any() in range (0, len(random_pixels)):
        #     # print(random_pixels)
        #     # if it's less than 0.5 make pixels white
        # if random_pixels.any() > 0.5:
        #     if not self.is_white:
        #         self.Canvas.create_rectangle(1, 1, 450, 8, fill="white", outline="white")
        #         # self.input_user_prompt.configure(bg="#E2E2E2")
        #         self.is_white = True

        #     # otherwise make pixels red
        #     else:
        #         # red produces best response 
        #         self.Canvas.create_rectangle(1, 1, 450, 8, fill="red", outline="red")
        #         # self.input_user_prompt.configure(bg="#FF0000")
        #         self.is_white = False
        
        # # 40ms (25Hz) produces best response
        # self.main_window.after(40, self.flickering_screen)


    def popup_display(self):
        # if no popup and should have popup, display it
        if not self.popup_root:
            self.popup_root = tk.Tk()  # create popup window
            popup_button = tk.Button(self.popup_root, text="You've hit a roadblock", font=("Verdana", 12), bg="yellow", command=exit)
            popup_button.pack()

    def popup_close(self):
        if self.popup_root:
            self.popup_root.destroy() # destroys pop up window
            self.popup_root = None

    def realtime(self):
        self.prompt = self.input_user_prompt.get(0.0, "end")
        self.output_charcount.delete(0.0, "end")
        self.output_wordcount.delete(0.0, "end")
        self.output_sentencecount.delete(0.0, "end")
        self.output_pagecount.delete(0.0, "end")
        self.output_standby.delete(0.0, "end")


        tempcount, charcount, self.wordcount, sentencecount, pagecount = 0, 0, 0, 0, 0
        dictionary = enchant.Dict("en_US")
        completeSentences = sent_tokenize(self.prompt)  # produces array of sentences
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

        charcount = len(self.prompt.replace('\n', ''))
        pagecount = len(self.prompt) // self.PAGE_LENGTH
        
        
        # case: user wrote or deleted nothing for 60s
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
        if charcount == 0 or self.last_charcount != charcount:
            # canvas = tk.Canvas(main_window, 450, 8)
            cursor = canvas.create_rectangle(5, 5, 450, 8, fill = "red", outline = "red")
            canvas.pack()
            last_charcount = charcount
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
    
        # put values in interface
        self.output_charcount.insert(tk.INSERT, charcount)
        self.output_wordcount.insert(tk.INSERT, self.wordcount)
        self.output_sentencecount.insert(tk.INSERT, sentencecount)
        self.output_pagecount.insert(tk.INSERT, pagecount)
        self.output_standby.insert(tk.INSERT, standbyNotification)

        # concatenate rows so dataframe is continuous
        self.keyboard_training_features = pd.concat([self.keyboard_training_features, self.history_dffeatures], axis=0)
        # print(self.keyboard_training_features)
        
        self.row_index += 1

        # create initial csv file for records
        if len(self.keyboard_training_features.index) == 1:
            self.keyboard_training_features.to_csv('keyboard.csv')
        
        # every 5s append one row to existing csv file to update records
        self.keyboard_training_features.loc[self.row_index - 1:self.row_index].to_csv('keyboard.csv', mode='a', header=False)

        # label is sum of all future data

        self.training_label = self.history_dffeatures["words produced"][-300:].sum()
        # print(self.training_label)

        # call realtime() every 5s
        self.main_window.after(5000, self.realtime)

        # update and return every 5s - outputs 1 row every 5s
        return self.keyboard_training_features # first training set - means, maxes, sums
        # return self.history_dffeatures # second training set - raw numbers
        # test both types of keyboard features in ml model and determine which has less error
        

if __name__ == '__main__':
    gui1 = gui()
    # gui1.flickering_screen()
    gui1.popup_display()
    gui1.popup_close()
    # main processing function
    gui1.realtime()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()