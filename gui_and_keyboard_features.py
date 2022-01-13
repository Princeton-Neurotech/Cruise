import time
import pandas as pd
import numpy as np
import tkinter as tk
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import exit
import machine_learning
import itertools as it

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
        self.time_last_change = time.time()
        self.PAGE_LENGTH = 4002
        self.roadblock = False
        self.nb_standby = 0
        self.wordcount_list = [0, ]
        self.total_wordcount_list = []
        
        self.time_for_features = time.time()
        self.history_time_seconds = []
        self.history_word_count = []
        self.history_sentence_count = []
        self.history_standby = []
        self.history_features = []
        self.history_dffeatures = []
        self.features_5s = 0

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
        # print("wordcount list:", self.wordcount_list)

        charcount = len(prompt.replace('\n', ''))
        pagecount = len(prompt) // self.PAGE_LENGTH
        
        # case: user wrote or deleted nothing for 60s
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
        if charcount == 0 or self.last_charcount != charcount:
            
            self.time_last_change = time.time()
            
        #print('TLC:', self.time_last_change, 'subs:', time.time() - self.time_last_change)
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
                self.history_dffeatures['5rSUMMARY_' + col] = self.history_dffeatures[col].rolling(5).mean() 
            elif col == "standby":
                self.history_dffeatures["5rSUMMARY_" + col] = self.history_dffeatures[col].rolling(5).max()
            elif col == "words produced" or col == "sentences produced" or col == "words deleted" or col == "sentences deleted" or col == "change in wordcount" or col == "change in sentencecount":
                self.history_dffeatures['5rSUMMARY_' + col] = self.history_dffeatures[col].rolling(5).sum() 
        # print(self.history_dffeatures)

        if round(time.time() - self.time_for_features, 2) > 5:
            every_5s_index = 3
            for every_5s_index in range (3, 60, 1):
                every_5s_data = self.history_dffeatures.iloc[[every_5s_index]]
                every_5s_index += 1
                print(every_5s_data)

        # put values in interface
        self.output_charcount.insert(tk.INSERT, charcount)
        self.output_wordcount.insert(tk.INSERT, self.wordcount)
        self.output_sentencecount.insert(tk.INSERT, sentencecount)
        self.output_pagecount.insert(tk.INSERT, pagecount)
        self.output_standby.insert(tk.INSERT, standbyNotification)

        # call realtime() every 5s
        self.main_window.after(5000, self.realtime)

        return self.wordcount_list

    """
    def lists_of_lists(self):
        overlap = 2
        window_length = 10 # 10s
        split = window_length / overlap # 5s
        batch_length = 60 # 60 batches every 5 min
        retrain_delay = 300 # 5 min
        num_batches = retrain_delay / batch_length # 300/10 * 2 (overlap)= 60

        self.total_wordcount_list.append(self.wordcount_list)
        self.wordcount_list = []
        self.main_window.after(5000, self.lists_of_lists)
        # print(self.total_wordcount_list)
        return self.total_wordcount_list
        
                index = 0
                beginning_intervals = 0
                for beginning_intervals in range (0, retrain_delay + 1, 5): 
                    beginning_intervals = beginning_intervals # beginning interval of each batch
                    end_intervals = beginning_intervals + 10 # end interval of each batch
                    for index in range (0, 1, 5):
                        self.intervals_array.insert(0, beginning_intervals)
                        self.intervals_array.insert(0, end_intervals)
                self.intervals_array.pop(0) # extra 310
                self.intervals_array.pop(1) # extra 305
                self.intervals_array.reverse() # was in reverse order beforehand

                # move across array in window fashion, printing each beginning and end interval pair
                def moving_window(x, length, step=1):
                    streams = it.tee(x, length)
                    return zip(*[it.islice(stream, i, None, step*length) for stream, i in zip(streams, it.count(step=step))])
                self.split_intervals_array = list(moving_window(self.intervals_array, 2))
                # print(self.split_intervals_array)
                self.np_split_intervals_array = np.array(self.split_intervals_array)
                dataframe = pd.DataFrame(self.np_split_intervals_array)
                dataframe["wordcount"] = ""
                print(dataframe)
        
    def every_5_min(self):
        # second list is 0-5, third is 5-10, fourth is 10-15, etc.
        # first two inner lists are unused, first interval wanted is 0-10
        keyboard_training_features = []
        wordcount_index = 1
        for i in range(2, len(self.total_wordcount_list), wordcount_index):
            # access second element of each inner list, most updated wordcount every 5s
            wordcount_in_interval = self.total_wordcount_list[i][1]
            keyboard_training_features.append(wordcount_in_interval)
            i += 1
        # print(keyboard_training_features)
        training_label = sum(keyboard_training_features[:-300])
        # print(training_label)
        
        
        curr_features = [sum(self.diff_wordcount_queue[301+i:300+5*i+5]) for i in range(5*60/5)]
        ml_prediction = []
        ml_label_predicted = ml_prediction.predict(curr_features) < wordcountThresholdInt
        if ml_label_predicted:
            if self.roadblock:
                self.popup_display()
            else:
                self.popup_close()
        """

        # self.main_window.after(300000, self.every_5_min) # run every 5 min


if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()
    # gui1.lists_of_lists()
    # gui1.every_5_min()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()