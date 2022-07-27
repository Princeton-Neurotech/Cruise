import pandas as pd
from regex import R
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, SGDClassifier, LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score, recall_score, mean_squared_error, f1_score, precision_recall_curve
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.inspection import PartialDependenceDisplay
import os

def rb_ml():
    data = pd.read_csv('keyboard1.csv')
    # data.columns = ["charcount", "wordcount", "sentencecount", "standby", "number of standby", "roadblock number", "chars prodocued", "words produced", "sentences produced", "chars deleted", "words deleted", "sentences deleted", "change in charcount", "change in wordcount", "change in sentencecount", "5rSUMMARY charcount", "5rSUMMARY wordcount", "5rSUMMARY sentencecount", "5rSUMMARY standby", "5rSUMMARY number of standby", "5rSUMMARY roadblock number", "5rSUMMARY words produced", "5rSUMMARY sentences produced", "5rSUMMARY words deleted", "5rSUMMARY sentences deleted", "5rSUMMARY change in wordcount", "5rSUMMARY change in sentencecount"]
    # print(data)
    # exported_data = data.to_csv('data.csv')
    # data = pd.read_csv('data.csv')
    # print(data.columns)
    data = data.dropna()

    # training and testing sets, 80/20 ratio
    label = data["standby"]
    label = label.shift(periods=-59)
    label = label.dropna()
    label = label.astype('int')

    data = data.drop("roadblock", axis=1)
    data = data.drop("5rSUMMARY roadblock number", axis=1)
    data = data.drop("5rSUMMARY standby", axis=1)
    data = data.drop("5rSUMMARY number of standby", axis=1)
    data = data.drop("roadblock number", axis=1)
    data = data.drop("Unnamed: 0", axis=1)

    data = data.shift(periods=59)
    # print(data)
    data = data.dropna()
    # print(data)
    # x_train_set, x_test_set, y_train_set, y_test_set = train_test_split(data, label, test_size=0.4, shuffle=False)
    x_train_set = data.iloc[:-59 , :]
    x_test_set = data.tail(59)
    y_train_set = label.iloc[:-59]
    y_test_set = label.tail(59)
    print(y_test_set)

    # models
    svc = SVC()
    logisitic_regression = LogisticRegression()
    sgd_classifier = SGDClassifier()
    decision_tree = DecisionTreeRegressor()
    random_forest_regressor = RandomForestRegressor()
    random_forest_classifier = RandomForestClassifier()
    linear_regression = LinearRegression()

    # fitting and predicting
    svc.fit(x_train_set, y_train_set)
    testing_predictions = svc.predict(x_test_set)

    # calculating error
    # mse = mean_squared_error(y_test_set, testing_predictions)
    # mse = np.sqrt(mse)
    # print(mse)

    # alternative to mse for classification ml model
    n_correct = sum(testing_predictions==y_test_set)
    print(n_correct/(len(x_test_set)))

    scores = cross_val_score(svc, x_test_set, y_test_set, scoring = "accuracy", cv=3)
    rmse_scores = np.sqrt(scores)
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())

    roadblock_precision_score = precision_score(y_test_set, testing_predictions)
    print(roadblock_precision_score)
    roadblock_recall_score = recall_score(y_test_set, testing_predictions)
    print(roadblock_recall_score)
    roadblock_f1_score = f1_score(y_test_set, testing_predictions)
    print(roadblock_f1_score)
    precision, recall, thresholds = precision_recall_curve(y_test_set, testing_predictions)
    # pr, tpr, thresholds = roc_curve(y_test_set, scores)
    # plt.plot(thresholds, precision[:-1], label='precision')
    # plt.plot(thresholds, recall[:-1], label='recall')
    # plt.show()
    # print(fpr)
    # print(tpr)

    # feature importance
    # random_forest.fit(x_train_set["wordcount"], label)
    # for name, score in zip(x_train_set["features_names"], random_forest.feature_importances_):
    # print(name, score)

    """
    # 5, 15, 16 are important
    importance = linear_regression.feature_importances_
    print(importance)
    # summarize feature importance
    for i,v in enumerate(importance):
        print('Feature: %0d, Score: %.5f' % (i,v))

    sorted_indices = np.argsort(importance)[::-1]
    print(sorted_indices)
    """

    # plt.title('Feature Importance')
    # plt.bar(range(x_train_set.shape[1]), importance[sorted_indices], align='center')
    # plt.xticks(range(x_train_set.shape[1]), x_train_set.columns[sorted_indices], rotation=90)
    # plt.tight_layout()
    # plt.show()


    # X, y = make_hastie_10_2(random_state=0)
    # clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(x_train_set, y_train_set)
    # features = [5, 6, (5, 6)]
    # PartialDependenceDisplay.from_estimator(clf, X, features)
    # plt.gcf()
    # plt.gca()
    # plt.use('Agg')
    """
    display = PartialDependenceDisplay.from_estimator(
        svc,
        x_train_set,
        features=["5rSUMMARY wordcount", "5rSUMMARY sentencecount", "5rSUMMARY standby", "5rSUMMARY number of standby", "5rSUMMARY words produced", "5rSUMMARY sentences produced", "5rSUMMARY words deleted", "5rSUMMARY sentences deleted", "5rSUMMARY change in wordcount", "5rSUMMARY change in sentencecount", "5rSUMMARY standby"],
        kind="both"
    )

    display.figure_.suptitle(
        "Partial dependence of house value on non-location features\n"
        "for the California housing dataset, with MLPRegressor"
    )
    """
    # display.figure_.subplots_adjust(hspace=0.3)

    # plt.savefig('name.png')
    # os.system('eog name.png &')

    confidence = 0.95
    squared_errors = (testing_predictions - y_test_set)**2
    confidence_interval = np.sqrt(stats.t.interval(confidence, len(squared_errors) - 1, loc=squared_errors.mean(), scale=stats.sem(squared_errors)))
    # print(confidence_interval)
    # print(testing_predictions)

    # search for best hyperparameters
    # grid_search = GridSearchCV(random_forest, param_grid, cv=[], scoring='r2', return_train_score=True)
    # grid_search.fit(x_train_set, y_train_set)
    
    print(testing_predictions)
    return testing_predictions[-1]

rb_ml()