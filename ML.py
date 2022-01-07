import time
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

class ml():

    """
    we need an initial set of 30 mins of training data, start out ML classifier on that 
    need to figure out length of feature vector input... 1 min? 30 seconds? etc. 
    append brain data together, add up wordcount so for productivity
    we have 30 mins of data 
    5 mins - > input that to algorithm to predict next 5 mins 
    @ 6 mins -> predict next 5 mins of productivity 
    get a guesstimate for produtivity in each minute, multiply by 5 
            
    TRAINING:
    we want to make predictions every 5 min
    use data @ time stamp x to predict word count @ x + 1
    as we are actively working (typing), every 5 minutes or so we wants to retrain our algorithm 
    using the batches of brain data/word count data we've collected over those 5 mins 
    slice creatively so we get lots of different feature vectors (double amount)

    our prediction is word count in the future
    """

    def __init__(self):
        self.X_df = pd.DataFrame() # features
        self.y_df = pd.DataFrame() # label
        self.ml_model = None

    def add_training_data(self, features, label):
        # check data is good - data is strictly positive
        if None in features or label == None:
            return
        self.X_df = self.X_df.append(features)
        self.y_df = self.X_df.append(label)

        # if length % 50 call train model to train every 50 

    def train_model():
        # update ml model
        self.X_df = RandomForestRegressor()

    def predict(features):
        # Return expected words per 5 minute
        # if model hasn't be created yet due to insufficient data don't show popup
        if not ml_model: return float('infinity')
        # if model exists use aggregated latest 300s from queue to predict future words
        return ml_model.predict(features)