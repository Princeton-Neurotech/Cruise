from gui_and_keyboard_feature_vectors import *
from brain_feature_vectors import *
from brain_data import *
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor


if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()
    gui1.main_window.mainloop()

    brain_data1 = brain_data()

    # feature vectors
    # keyboard input data: keyboard_input_fv
    # brain data: brain_fv
    all_feature_vectors = keyboard_input_fv.append(brain_fv)


