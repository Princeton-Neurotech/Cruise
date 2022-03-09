import time
import pandas as pd
import numpy as np

import only_keyboard_features 
import brain_data_collection

from sklearn import decomposition
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

    def process_data(self):
            self.features_list = ['mean_0', 'mean_d_h2h1_0', 'mean_q1_0', 'mean_q2_0', 'mean_q3_0',
                              'mean_q4_0', 'mean_d_q1q2_0', 'mean_d_q1q3_0', 'mean_d_q1q4_0',
                              'mean_d_q2q3_0', 'mean_d_q2q4_0', 'mean_d_q3q4_0', 'std_0',
                              'std_d_h2h1_0', 'max_0', 'max_d_h2h1_0', 'max_q1_0', 'max_q2_0',
                              'max_q3_0', 'max_q4_0', 'max_d_q1q2_0', 'max_d_q1q3_0', 'max_d_q1q4_0',
                              'max_d_q2q3_0', 'max_d_q2q4_0', 'max_d_q3q4_0', 'min_0', 'min_d_h2h1_0',
                              'min_q1_0', 'min_q2_0', 'min_q3_0', 'min_q4_0', 'min_d_q1q2_0',
                              'min_d_q1q3_0', 'min_d_q1q4_0', 'min_d_q2q3_0', 'min_d_q2q4_0',
                              'min_d_q3q4_0', 'topFreq_1_0', 'topFreq_2_0', 'topFreq_3_0',
                              'topFreq_4_0', 'topFreq_5_0', 'topFreq_6_0', 'topFreq_7_0',
                              'topFreq_8_0', 'topFreq_9_0', 'topFreq_10_0', 'freq_011_0',
                              'freq_021_0', 'freq_032_0', 'freq_043_0', 'freq_053_0', 'freq_064_0',
                              'freq_075_0', 'freq_085_0', 'freq_096_0', 'freq_107_0', 'freq_117_0',
                              'freq_128_0', 'freq_139_0', 'freq_149_0', 'freq_160_0']
            self.brain_training_features = pd.DataFrame(columns=self.features_list)
            # standardize the data
            eeg_brain_data_stand = StandardScaler().fit_transform(eeg_brain_data)
            print(eeg_brain_data_stand)

            ml_brain = brain_data_collection.braindata()
            # PCA to reduce dimensionality from 5104 to low hundreds features
            pca = decomposition.PCA(n_components=8, svd_solver='full')
            pca.fit(ml_brain.eeg_brain_data)
            pca_eeg_brain_data = pca.transform(ml_brain.eeg_brain_data)

            print("Number of features: " + str(pca.n_features_))
            print("Number of samples: " + str(pca.n_samples_))
            pca_eeg_brain_data = pca.transform(eeg_brain_data_stand)

            # correlations between a component each feature (each component is a linear combination of given features)
            print("Correlations between each feature and each component")
            print(pd.DataFrame(pca.components_, columns=eeg_brain_data.columns))

            # number of components
            print("Number of components selected: " + str(pca.components_.shape[0]))

            # percent of variance explained by each component (descending order)
            print(pca.explained_variance_ratio_)

            if len(total_brain_data) != 0 and len(total_brain_data[0]) > 5:
                # 5104 columns, 8 channels, 638 different data computations applied
                eeg_computations = brain_data_computations.calc_feature_vector(total_brain_data.T)
                print(eeg_computations)

                try:
                    self.brain_training_features.columns = eeg_computations[-1]
                except ValueError:
                    self.brain_training_features = pd.DataFrame(columns=eeg_computations[-1])
                self.brain_df = pd.DataFrame(columns=eeg_computations[-1])

                # every 5s collect one row of data
                if (int(time.time() - self.start_time)) % 5 == 1.0 and (int(time.time() - self.start_time)) != 0:
                    self.is_5s = True
                elif (int(time.time() - self.start_time)) % 5 == 0.0 and (int(time.time() - self.start_time)) != 0 and self.is_5s == True:

                    # mean of each column based on number of rows outputted every 5s
                    mean_brain = self.appended_summary_brain_df.iloc[:self.appended_summary_brain_df.shape[0]].mean(
                        axis=0)
                    # mean returns a pandas series, convert back to dataframe
                    mean_brain_df = mean_brain.to_frame()
                    # opposite dimensions, transpose
                    self.transposed_mean_brain_df = mean_brain_df.T

                    # append so dataframe continuously grows for 5 min
                    self.brain_training_features.loc[len(
                        self.brain_training_features)] = eeg_computations[0]
                    self.is_5s = False
                    self.row_index += 1
                    print(self.brain_training_features)

    def read_csv(self):
        ml_keyboard = gui_and_keyboard_features.gui()
        self.keyboard_training_features = pd.DataFrame()
        self.brain_traning_features = pd.DataFrame()
    
        # print one row of keyboard and brain data every 5s for 5 min
        self.keyboard_training_features = ml_keyboard.only_keyboard_features.append(ml_keyboard.only_keyboard_features)       
        print(self.keyboard_training_features)
        self.brain_training_features = ml_brain.brain_data_collection.append(ml_brain.brain_data_collection)
        print(self.brain_training_features)

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