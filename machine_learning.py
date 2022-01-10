import time
import pandas as pd
import numpy as np

import gui_and_keyboard_features 
import running_and_brain_features

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

class ml():

    """
    Need an initial set of 30 mins of training data, start out ML classifier on that 
    Need to figure out length of feature vector input... 1 min? 30 seconds? etc. 
    Append wordcount and brain data together, making sure timeframe is same so rows are equal 
    5 mins - > input that to algorithm to predict next 5 mins 
    @ 6 mins -> predict next 5 mins of productivity 
    Get a guesstimate for produtivity in each minute, multiply by 5 
            
    TRAINING:
    Want to make predictions every 5 min
    Use data @ time stamp x to predict word count @ x + 1
    As one is actively working (typing), every 5 minutes, want to retrain algorithm 
    using the batches of wordcount/brain data collected over those 5 mins 
    slice creatively so we get lots of different feature vectors (double amount)

    Our prediction is wordcount in the future (label)
    """

    def __init__(self):
        ml_keyboard_data = gui_and_keyboard_features.gui()
        ml_brain_data = running_and_brain_features.braindata()

        self.features = []
        self.features.append(ml_keyboard_data.keyboard_training_features) # add keyboard features
        self.features.append(ml_brain_data.brain_training_features) # add brain features

        self.label = ml_keyboard_data.training_label

        self.X_df = pd.DataFrame()
        self.y_df = pd.DataFrame()

        self.ml_model = None

        self.train_set, self.test_set = train_test_split(self.features, test_size=0.2, random_state=42)

    def add_training_data(self, train_set, label):
        # check data is good - data is strictly positive
        if None in train_set or label == None:
            return
        self.X_df = self.X_df.append(train_set)
        self.X_df.columns = ['wordcount', 'brain data']

        self.y_df = pd.DataFrame(label, columns = ['label']) # add label - only keyboard

    # if length % 120 call train model to train every 300s
    def train_model(self):
        # update ml model
        self.ml_model = RandomForestRegressor()
        self.ml_model.fit(self.X_df, self.y_df)

    def predict(self):
        # Return expected words per 5 minute
        # if model hasn't be created yet due to insufficient data don't show popup
        if not self.ml_model: return float('infinity')
        # if model exists use aggregated latest 300s from queue to predict future words
        training_predictions = self.ml_model.predict(self.X_df)
        mse = mean_squared_error(self.y_df, self.X_df)
        mse = np.sqrt(mse)

        scores = cross_val_score(self.ml_model, self.X_df, self.y_df, scoring = "neg_mean_squared_error", cv=10)
        rmse_scores = np.sqrt(-scores)
        print("Scores:", scores)
        print("Mean:", scores.mean())
        print("Standard deviation:", scores.std())