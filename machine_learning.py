import time
import pandas as pd
import numpy as np

import gui_and_keyboard_features 
import final_brain_features

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

    def __init__(self):
        self.csv_index = 0

    def read_csv(self):
        print("Julian")
        ml_keyboard = gui_and_keyboard_features.gui()
        print("1")
        print(ml_keyboard.keyboard_training_features)
        ml_brain = final_brain_features.braindata()

        self.keyboard_training_features = pd.DataFrame()
        self.brain_traning_features = pd.DataFrame()
    
        # print one row of keyboard and brain data every 5s for 5 min
        self.keyboard_training_features = ml_keyboard.keyboard_training_features.append(ml_keyboard.keyboard_training_features)       
        # print(self.keyboard_training_features)
        self.brain_training_features = ml_brain.brain_training_features.append(ml_brain.brain_training_features)
        # print(self.brain_training_features)

        # should be 60 rows (each worth 5s) by 70 columns (7 for keyboard + 63 for brain data)
        # self.every_5_min_combined = pd.concat([every_5_min_keyboard, every_5_min_brain], axis=1)
        # print(self.every_5_min_combined)

        # for self.i in range (0, 1000000):
            # choose 60 rows, after one iteration, choose 0 to the next 60 rows
            # every_5_min_keyboard = every_5_min_keyboard.iloc[0:60*self.i]
            # every_5_min_brain = every_5_min_brain.iloc[0:60*self.i]
            
        # self.label = ml_keyboard_data.training_label # add label
        # self.ml_model = None

    def add_training_data(self):
        # training and testing sets, 80/20 ratio
        # remove words produced column since it's our label
        self.x_train_set, self.y_train_set, self.x_test_set, self.y_test_set = train_test_split(self.every_5_min_combined.drop['5rSUMMARY words produced'], self.label, test_size=0.2, random_state=42)

        # find best combination of hyperparameter values (setup)
        # param_grid = ['n_estimators': [], 'max_features': [] ]

    def train_model(self):
        # update ml model...
        
        self.ml_model = RandomForestRegressor()
        self.ml_model.fit(self.x_train_set, self.y_train_set)

        # ensemble learning through using random forest classifier?
        # self.ml_model = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)
        # self.ml_model.fit(self.x_train_set, self.y_train_set)

        # or for feature importance: 
        # self.ml_model.fit(self.x_train_set["data"], self.x_train_set["target"]])
        # for name, score in zip(self.x_train_set["features_names"], self.ml_model.feature_importances_):
            # print(name, score)

        # search for best hyperparameters
        # grid_search = GridSearchCV(self.ml_model, param_grid, cv=[], scoring='neg_mean_squared_error', return_train_score=True)
        # grid_search.fit(self.x_train_set, self.y_train_set)

    def predict(self):
        # return expected words produced every 5 minutes
        # if model hasn't be created yet due to insufficient data don't show popup
        if not self.ml_model: return float('infinity')
        
        # if model exists use aggregated latest 300s from queue to predict future words produced
        training_predictions = self.ml_model.predict(self.x_test_set)
        mse = mean_squared_error(self.y_test_set, training_predictions)
        mse = np.sqrt(mse)

        scores = cross_val_score(self.ml_model, training_predictions, self.y_test_set, scoring = "neg_mean_squared_error", cv=10)
        rmse_scores = np.sqrt(-scores)
        # print("Scores:", scores)
        # print("Mean:", scores.mean())
        # print("Standard deviation:", scores.std())
        
"""
if __name__ == "__main__":
    myml = ml()
    # myml.add_raw_data()
    # myml.add_training_data()
    # myml.train_model()
    # myml.predict()
"""