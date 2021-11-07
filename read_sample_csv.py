import pandas as pd
import matplotlib.pyplot as plt

orig_folder = 'Data'
input_data = 'Data/example_single_person_single_reading.csv'
data = pd.read_csv(input_data)

# 250Hz update rate, 24x gain
# https://docs.openbci.com/Cyton/CytonDataFormat/
scale = 4.5 / 24 / (2^23 - 1)
eeg_data = data.iloc[1:,1:9]*scale
eeg_data = eeg_data - eeg_data.iloc[0,:] # centre data
eeg_data.iloc[0,:]
scale = 4.5 / 24 / (2^23 - 1)

plt.plot(eeg_data)
plt.legend()
plt.show()
# still some drift to deal with

