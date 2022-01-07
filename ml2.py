import time
import pandas as pd
import numpy as np



class ml2():
    """
    """

    def __init__(self):
        self.X_df = pd.DataFrame()
        self.y_df = pd.DataFrame()
        self.ml_model = None

    def add_training_data(features, label):
        # check data is good - data is strictly positive
        if None in features or label==None:
            return
        self.X_df = self.X_df.append(features)
        self.y_df = self.y_df.append(label)

        # if length % 50 call train model to train every 50 

    def train_model():
        # update ml model
    
    def predict(features):
        """Return expected words per 5 minute"""
        # if model hasn't be created yet due to insufficinet data don't show popup
        if not ml_model: return float('infinity')
        # if model exists use aggregated latest 300s from queu to pedict future wo
        return ml_model.predict(features)