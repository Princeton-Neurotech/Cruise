import multiprocessing
import workers
import web_interface
import matplotlib.pyplot as plt
from multiprocessing import Manager
from sklearn import decomposition
from sklearn import preprocessing
import pandas as pd
# from scipy.stats import linregress
# increase recursion limit
# sys.setrecursionlimit(15000)
 
def keyboard_process():
  proc1 = multiprocessing.Process(target=workers.worker1, args=(ns,))
  proc1.start() 

def brain_data_process(board,ns):
  proc2 = multiprocessing.Process(target=workers.worker2, args=(board,ns))
  proc2.start()

# def timing():
"""
  to determine timing to concatenate dataframes
  brain_points = []
  keyboard_points = []
  timescale = []
  for i in range(10):
    time.sleep(5)
    brain_points.append(len(ns.brain_df))
    keyboard_points.append(len(ns.keyboard_df))
    timescale.append(5*i)
    print([len(ns.brain_df), len(ns.keyboard_df)])
  plt.plot(brain_points, timescale)
  plt.plot(keyboard_points, timescale)
  linregress(timescale, brain_points)
  linregress(timescale, keyboard_points)
  # brain_slope, brain_intercept = l
  # keyboard_slope, keyboard_intercept = 
  # print("y = " + brain_slope + "*x " + brain_intercept)
  # print("y = " + keyboard_slope + "*x " + keyboard_intercept)
  plt.show()
  # plt.legend()
"""
# def selenium():
#     print("process 1")
#     mySelenium = web_interface.selenium()
#     myList = mySelenium.connectSelenium()
#     myUID = myList[0]
#     myDriver = myList[1]

def interface_process(mySelenium, myUID): 
  print("process 2")  
  proc3 = multiprocessing.Process(target=workers.worker3, args=[mySelenium, myUID])
  # p = multiprocessing.Process(target=selenium)
  # p.start()
  proc3.start()
  # proc3.terminate()
  # if hrs == 1.5:
    # namespace.keyboard.to_csv('keyboard.csv', mode='a', header=False)

def ml_analysis(namespace):
  # pca to reduce dimensionality from 5104 to low hundreds features
  pca = decomposition.PCA(n_components=8, svd_solver='full')
  pca.fit(namespace.keyboard)
  pca_keyboard = pca.transform(namespace.keyboard)

  print("Number of features: " + str(pca.n_features_))
  print("Number of samples: " + str(pca.n_samples_))

  # correlations between a component each feature (each component is a linear combination of given features)
  print("Correlations between each feature and each component")
  print(pd.DataFrame(pca.components_, columns=namespace.keyboard.columns))

  # number of components
  print("Number of components selected: " + str(pca.components_.shape[0]))

  # percent of variance explained by each component (descending order)
  print(pca.explained_variance_ratio_)

  # standardize the data
  standardized_keyboard = preprocessing.StandardScaler().fit_transform(standardized_keyboard)
  print(standardized_keyboard)

def timing_process():
  proc4 = multiprocessing.Process(target=workers.worker4)
  proc4.start()

"""
def main():
  mgr = Manager()
  ns = mgr.Namespace()
  # don't run keyboard_process, realtime() is ran within worker 3 in processSelenium
  # keyboard_process()
  mySelenium = web_interface.selenium()
  myList = mySelenium.connectSelenium()
  myUID = myList[0]
  myDriver = myList[1]
  interface_process(mySelenium,myUID)
  # mySelenium.closeSelenium(myDriver)
"""

# run keyboard and interface concurrently to collect ml data
if __name__ == "__main__":
  mgr = Manager()
  ns = mgr.Namespace()
  # don't run keyboard_process, realtime() is ran within worker 3 in processSelenium
  # keyboard_process()
  mySelenium = web_interface.selenium()
  myList = mySelenium.connectSelenium()
  myUID = myList[0]
  myDriver = myList[1]
  interface_process(mySelenium,myUID)
  mySelenium.closeSelenium(myDriver)
  
# freeze_support()
# myBoard = brain_data_collection.braindata(38, "/dev/cu.usbserial-DM03H3ZF")
# need to have filled dataframe that we will later replace its values 
# ns.brain = pd.DataFrame(np.zeros((1,4)))
# print(ns.brain)
# brain_data_process(myBoard, ns)
# while True:
#   print(ns.brain)

# to decrease number of rows of brain data since # points of brain data > # points keyboard data
# rolling mean of 256 rows because sampling rate is 256 and getting keyboard data every 1s
# mean_brain = myBoard.brain_df.rolling(256, min_periods=1).mean() 
# mean returns a pandas series, convert back to dataframe
# mean_brain_df = mean_brain.to_frame()
# print(mean_brain_df)
# opposite dimensions, transpose
# transposed_mean_brain_df = mean_brain_df.T