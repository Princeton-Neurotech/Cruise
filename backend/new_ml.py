import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.metrics import mean_squared_error

data = pd.read_csv('keyboard.csv')
data.columns = ["charcount", "wordcount", "sentencecount", "standby", "number of standby", "roadblock number", "chars prodocued", "words produced", "sentences produced", "chars deleted", "words deleted", "sentences deleted", "change in charcount", "change in wordcount", "change in sentencecount", "5rSUMMARY charcount", "5rSUMMARY wordcount", "5rSUMMARY sentencecount", "5rSUMMARY standby", "5rSUMMARY number of standby", "5rSUMMARY roadblock number", "5rSUMMARY words produced", "5rSUMMARY sentences produced", "5rSUMMARY words deleted", "5rSUMMARY sentences deleted", "5rSUMMARY change in wordcount", "5rSUMMARY change in sentencecount"]
#print(data)

label = data["5rSUMMARY roadblock number"]
# training and testing sets, 80/20 ratio
kinda_label = data["roadblock number"]
data = data.drop("roadblock number", axis=1)
x_train_set, x_test_set, y_train_set, y_test_set = train_test_split(data.drop("5rSUMMARY roadblock number", axis=1), label, test_size=0.2, random_state=42)
ml_model = RandomForestRegressor()
# print(x_train_set)
# print("y set")
# print(y_train_set)
ml_model.fit(x_train_set, y_train_set)
training_predictions = ml_model.predict(x_test_set)
# print(training_predictions)
# x_train_set = x_train_set.reshape(1, -1)
# x_test_set = x_test_set.reshape(1, -1)
mse = mean_squared_error(y_test_set, training_predictions)
mse = np.sqrt(mse)
# print(mse)
scores = cross_val_score(ml_model, x_test_set, y_test_set, scoring = "neg_mean_squared_error", cv=10)
rmse_scores = np.sqrt(-scores)
print("Scores:", scores)
print("Mean:", scores.mean())
print("Standard deviation:", scores.std())

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