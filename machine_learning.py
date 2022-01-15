import time
import pandas as pd
import numpy as np

import gui_and_keyboard_features 
import running_and_brain_features

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.datasets import load_iris

class ml():

    """
    Initial set of 30 mins / 1 hr of training data: start out ML classifier on that 
    Length of feature vector input: need to calculate number of rows in each dataframe
    Append keyboard and brain data together, making sure timeframe is same so rows are equal 
    5 mins - > input that to algorithm to predict next 5 mins 
    @ 6 mins -> predict next 5 mins of productivity - are we retraining and predicting every 1 or 5 min?
    Get a guesstimate for produtivity in each minute, multiply by 5 
            
    TRAINING:
    Want to make predictions every 5 min
    Use data @ time stamp x to predict word count @ x + 1
    As one is actively working (typing), every 5 minutes, want to retrain algorithm 
    using the batches of wordcount/brain data collected over those 5 mins 
    slice creatively so we get lots of different feature vectors (double amount)

    Our prediction is wordcount in the future (label)
    """
    
    # TO-DO:
    # add columns to both dataframes that will match up and merge them based on this condition

    def __init__(self):
        ml_keyboard_data = gui_and_keyboard_features.gui()
        ml_brain_data = running_and_brain_features.braindata()

        self.features = pd.DataFrame()
        self.features.append(ml_keyboard_data.keyboard_training_features) # add keyboard features
        self.features.append(ml_brain_data.compressed_brain_training_features) # add brain features
    
        # transpose dataframe so that 60 rows now become 60 columns - each containing 5s of data
        self.features_dict = {'features': self.features}
        self.features_before_transposed = pd.DataFrame(data=self.features_dict)
        self.features_after_transposed = self.features_before_transposed.T
        print(self.features_after_transposed)

        self.label = ml_keyboard_data.training_label # add label

        self.X_df = pd.DataFrame()
        self.y_df = pd.DataFrame()

        self.ml_model = None

        self.train_set = []

    def add_training_data(self):
        # check if data is good
        if None in self.train_set or self.label == None:
            return
        
        self.train_set, self.test_set = train_test_split(self.features, test_size=0.2, random_state=42)
        
        self.X_df = self.X_df.append(self.train_set)
        self.X_df.columns = ['keyboard data', 'brain data']

        self.y_df = pd.DataFrame(self.label, columns = ['label']) # add label - only keyboard data

        # find best combination of hyperparameter values (setup)
        # param_grid = ['n_estimators': [], 'max_features': [] ]

    # if length % 120 call train model to train every 300s
    def train_model(self):
        # update ml model
        self.ml_model = RandomForestRegressor()
        self.ml_model.fit(self.X_df, self.y_df)
        # ensemble learning through using random forest classifier?
        self.ml_model = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)
        self.ml_model.fit(self.X_df, self.y_df)

        # or for feature importance: 
        # self.ml_model.fit(iris["data", iris["target"]])
        # for name, score in zip(iris["features_names"], self.ml_model.feature_importances_):
            # print(name, score)

        # search for best hyperparameters
        # grid_search = GridSearchCV(self.ml_model, param_grid, cv=[], scoring='neg_mean_squared_error', return_train_score=True)
        # grid_search.fit(self.X_df, self.y_df)

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
        # print("Scores:", scores)
        # print("Mean:", scores.mean())
        # print("Standard deviation:", scores.std())

if __name__ == "__main__":
    myml = ml()
    myml.add_training_data()
    myml.train_model()
    myml.predict()