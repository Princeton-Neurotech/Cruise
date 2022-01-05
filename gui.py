import time
import tkinter as tk
import numpy as np
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import exit

class gui():

    def __init__(self):
        self.PAGE_LENGTH = 4002

        self.global_charcount = 0
        self.global_wordcount = 0
        self.global_sentencecount = 0
        self.global_pagecount = 0

        self.time_last_change = time.time()
        self.time_roadblock = time.time()
        self.start_time = time.time()

        self.popup_root = None

        self.total_charcount = []
        self.total_word_count = []
        self.total_sentence_count = []
        self.total_page_count = []
        self.total_standby = []

        self.roadblock = False
        self.nb_standby = 0

        # Create interface
        self.main_window = tk.Tk()
        self.main_window.title("Roadblocks Project")
        self.main_window.geometry("500x600")

        # Textbox for prompt
        promptLabel = tk.Label(self.main_window, text="Write prompt here")
        self.input_user_prompt = tk.Text(self.main_window, width=450, height=8, font=("Times New Roman", 12), wrap="word")

        # Textbox for wordcount threshold
        wordcountThresholdLabel = tk.Label(self.main_window, text="Wordcount threshold")
        self.input_user_wordcount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12), wrap="word")

        pagecountThresholdLabel = tk.Label(self.main_window, text="Page count threshold")
        self.input_user_pagecount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12), wrap="word")

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
        self.input_user_wordcount_threshold.pack()

        pagecountThresholdLabel.pack()
        self.input_user_pagecount_threshold.pack()

        begin.pack()

    def popup_display(self):
        print("roadblock:", self.roadblock)
        # MAKE NOTIFICATION NOT COME UP IMMEDIATELY
        # if no popup and should have popup, display it
        if not self.popup_root:
            self.popup_root = tk.Tk() # create popup window
            popupButton = tk.Button(self.popup_root, text="You've hit a roadblock", font=("Verdana", 12), bg="yellow", command=exit)
            popupButton.pack()

    def popup_close(self):
        if self.popup_root:
            self.popup_root.destroy() # destroys pop up window
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
        try: wordcountThresholdInt = int(self.input_user_wordcount_threshold.get(0.0, "end"))
        except: pass
        try: pagecountThresholdInt = int(self.input_user_pagecount_threshold.get(0.0, "end"))
        except: pass

        # roadblock popup if haven't written enough words or pages
        self.roadblock = wordcount < wordcountThresholdInt or pagecount < pagecountThresholdInt
        if self.roadblock:
            self.popup_display()
        else:
            self.popup_close()

        print("condition:", wordcount < wordcountThresholdInt)
        
        pagecount = len(prompt) // self.PAGE_LENGTH
        charcount = len(prompt.replace('\n',''))

        # if anything has changed since last time update it and update time of last change
        if charcount != self.global_charcount or wordcount != self.global_wordcount or sentencecount != self.global_sentencecount:
            self.time_last_change = time.time()
            self.global_charcount = charcount
            self.global_wordcount = wordcount
            self.global_sentencecount = sentencecount
        
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
        self.total_page_count.append(pagecount)
        self.total_sentence_count.append(sentencecount)
        self.total_word_count.append(wordcount)
        self.total_charcount.append(charcount)
        self.total_standby.append(self.nb_standby)

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