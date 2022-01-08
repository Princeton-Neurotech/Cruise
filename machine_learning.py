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
        ml_gui = gui_and_keyboard_features.gui()
        ml_braindata = running_and_brain_features.braindata()
        self.keyboard_training_features = ml_gui.keyboard_training_features
        self.keyboard_training_label = ml_gui.keyboard_training_label
        self.brain_training_features = ml_braindata.brain_training_features
        self.x_df = pd.DataFrame(self.keyboard_training_features) # features
        self.x_df = self.x_df.append(ml_braindata.brain_training_features) # features
        self.x_df.columns = ['wordcount', 'brain data']
        self.y_df = pd.DataFrame(self.keyboard_training_label, columns = ['label']) # label
        self.ml_model = None

    def add_training_data(self, features, label):
        # check data is good - data is strictly positive
        if None in features or label == None:
            return
        self.x_df = self.x_df.append(features)
        self.y_df = self.X_df.append(label)

        # if length % 50 call train model to train every 50 

    def train_model(self):
        # update ml model
        self.x_df = RandomForestRegressor()

    def predict(features):
        # Return expected words per 5 minute
        # if model hasn't be created yet due to insufficient data don't show popup
        if not ml_model: return float('infinity')
        # if model exists use aggregated latest 300s from queue to predict future words
        return ml_model.predict(features)