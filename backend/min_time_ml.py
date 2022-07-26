import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.inspection import PartialDependenceDisplay

def machine_learning(wordcount):
    data = pd.read_csv('keyboard1.csv')
    # data.columns = ["charcount", "wordcount", "sentencecount", "standby", "number of standby", "roadblock number", "chars prodocued", "words produced", "sentences produced", "chars deleted", "words deleted", "sentences deleted", "change in charcount", "change in wordcount", "change in sentencecount", "5rSUMMARY charcount", "5rSUMMARY wordcount", "5rSUMMARY sentencecount", "5rSUMMARY standby", "5rSUMMARY number of standby", "5rSUMMARY roadblock number", "5rSUMMARY words produced", "5rSUMMARY sentences produced", "5rSUMMARY words deleted", "5rSUMMARY sentences deleted", "5rSUMMARY change in wordcount", "5rSUMMARY change in sentencecount"]
    # print(data)
    # exported_data = data.to_csv('data.csv')
    # data = pd.read_csv('data.csv')
    # print(data.columns)

    # training and testing sets, 80/20 ratio
    data = data.dropna()
    data = data.drop('new', axis=1)
    label = data["min time (s)"]
    data = data.drop("min time (s)", axis=1)
    data = data.drop("Unnamed: 0", axis=1)
    data = data['wordcount']
    data = pd.DataFrame(data, columns= ['wordcount'])

    x_train_set, x_test_set, y_train_set, y_test_set = train_test_split(data, label, test_size=0.2, random_state=42)

    # models
    decision_tree = DecisionTreeRegressor()
    random_forest = RandomForestRegressor()
    linear_regression = LinearRegression()

    # fitting and predicting
    linear_regression.fit(x_train_set, y_train_set)
    testing_predictions = linear_regression.predict(x_test_set)

    # calculating error
    mse = mean_squared_error(y_test_set, testing_predictions)
    mse = np.sqrt(mse)
    print(mse)

    scores = cross_val_score(linear_regression, x_test_set, y_test_set, scoring = "r2", cv=10)
    rmse_scores = np.sqrt(scores)
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())

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
        random_forest,
        x_train_set,
        features=["5rSUMMARY wordcount", "5rSUMMARY sentencecount", "5rSUMMARY standby", "5rSUMMARY number of standby", "5rSUMMARY words produced", "5rSUMMARY sentences produced", "5rSUMMARY words deleted", "5rSUMMARY sentences deleted", "5rSUMMARY change in wordcount", "5rSUMMARY change in sentencecount"],
        kind="both"
    )

    display.figure_.suptitle(
        "Partial dependence of house value on non-location features\n"
        "for the California housing dataset, with MLPRegressor"
    )
    display.figure_.subplots_adjust(hspace=0.3)

    plt.savefig('name.png')
    os.system('eog name.png &')
    """

    # confidence = 0.95
    # squared_errors = (testing_predictions - y_test_set)**2
    # confidence_interval = np.sqrt(stats.t.interval(confidence, len(squared_errors) - 1, loc=squared_errors.mean(), scale=stats.sem(squared_errors)))
    # print(confidence_interval)
    # print(testing_predictions)

    # search for best hyperparameters
    # grid_search = GridSearchCV(random_forest, param_grid, cv=[], scoring='r2', return_train_score=True)
    # grid_search.fit(x_train_set, y_train_set)

    # completion_buffer = open("thr.buf", 'r')
    # thresholds = completion_buffer.readlines()
    # wordcount = int(thresholds[0])
    ynew_list = [[int(wordcount)]]
    # ynew_list = np.array([wordcount, 0, 0, 0], [wordcount, 0, 0, 0])
    # ynew_list.reshape(-1, 1)
    print(ynew_list)
    ynew = linear_regression.predict(ynew_list)
    print(ynew)
    return ynew
    # print("ynew_list: ", ynew_list)
