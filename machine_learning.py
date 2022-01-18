import time
import pandas as pd
import numpy as np

import brain_data_computations
import gui_and_keyboard_features 
import brain_features

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
        print("machine learning")
        # ml_keyboard_data = gui_and_keyboard_features.gui()
        # ml_brain_data = brain_features.braindata(-1, "COM3")

        # while (int(time.time() - self.start_time) % 10 == 0) and (int(time.time() - self.start_time) != 0):
        # while True:
        # print("machine learning")

    def read_csv(self):
        # read csv file and make into pandas dataframe
        every_5_min_keyboard = pd.read_csv(("keyboard " + str(self.csv_index) + ".csv"))
        every_5_min_brain = pd.read_csv(("brain " + str(self.csv_index) + ".csv"))
        self.csv_index += 1

        for self.i in range (0, 1000000):
            # choose 60 rows, after one iteration, choose 0 to the next 60 rows
            every_5_min_keyboard = every_5_min_keyboard.iloc[0:60*self.i]
            every_5_min_brain = every_5_min_brain.iloc[0:60*self.i]

        # should be 60 rows (each worth 5s) by 70 columns (7 for keyboard + 63 for brain data)
        self.every_5_min_combined = pd.concat([every_5_min_keyboard, every_5_min_brain], axis=1)
        print(self.every_5_min_combined)

        ml_keyboard_data = gui_and_keyboard_features.gui()
        self.label = ml_keyboard_data.training_label # add label
        self.ml_model = None

    def add_training_data(self):
        # training and testing sets, 80/20 ratio
        # remove words produced column since it's our label
        self.x_train_set, self.y_train_set, self.x_test_set, self.y_test_set = train_test_split(self.every_5_min_combined.drop['5rSUMMARY words produced'], self.label, test_size=0.2, random_state=42)

        # find best combination of hyperparameter values (setup)
        # param_grid = ['n_estimators': [], 'max_features': [] ]

    def train_model(self):
        # update ml model
        self.ml_model = RandomForestRegressor()
        self.ml_model.fit(self.x_train_set, self.y_train_set)
        # ensemble learning through using random forest classifier?
        # self.ml_model = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)
        # self.ml_model.fit(self.x_train_set, self.y_train_set)

        # or for feature importance: 
        # self.ml_model.fit(iris["data", iris["target"]])
        # for name, score in zip(iris["features_names"], self.ml_model.feature_importances_):
            # print(name, score)

        # search for best hyperparameters
        # grid_search = GridSearchCV(self.ml_model, param_grid, cv=[], scoring='neg_mean_squared_error', return_train_score=True)
        # grid_search.fit(self.X_df, self.y_df)

    def predict(self):
        # return expected words per 5 minute
        # if model hasn't be created yet due to insufficient data don't show popup
        if not self.ml_model: return float('infinity')
        
        # if model exists use aggregated latest 300s from queue to predict future words
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

    def add_raw_data(self):
        start_time = time.time()
        while (int(time.time() - start_time) % 10 == 0.0) and (int(time.time() - start_time) != 0):
            print("machine learning")
            ml_keyboard_data = gui_and_keyboard_features.gui()
            ml_brain_data = brain_features.braindata(-1, "COM3")
            self.features = pd.DataFrame()
            self.features = self.features.append(ml_keyboard_data.keyboard_training_features) # add keyboard features
            self.features = self.features.append(ml_brain_data.compressed_brain_training_features) # add brain features
            # print(self.features)
        
    transpose dataframe so that 60 rows now become 60 columns - each containing 5s of data
    self.features_dict = {'features': self.features}
    print(self.features_dict)

    self.features_before_transposed = pd.DataFrame(data=self.features_dict)
    self.features_after_transposed = self.features_before_transposed.T
    print(self.features_after_transposed)
"""