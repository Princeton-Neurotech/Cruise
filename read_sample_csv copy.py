#Import statements
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, iirnotch

orig_folder = 'Data'
input_data = 'Data/sample2.csv'
data = pd.read_csv(input_data)

# 250Hz update rate, 24x gain
# https://docs.openbci.com/Cyton/CytonDataFormat/
scale = 4.5 / 24 / (2^23 - 1)
eeg_data = data.iloc[2500:,1:9]*scale # get rid of first 2.5s
# eeg_data = eeg_data - eeg_data.iloc[0,:] # centre data
eeg_data.iloc[0,:]

# still some drift to deal with

# plt.plot(data.iloc[1:,12:19])
# plt.show()



#%%
import mne
import numpy as np

np_eeg = eeg_data.to_numpy().reshape((8,-1))
output_data = mne.filter.filter_data(data = np_eeg, sfreq = 250, l_freq=7, h_freq=13)
output_data = mne.filter.notch_filter(x=output_data, Fs=250, freqs=np.arange(60, 120, 60))
output_data = output_data.reshape((-1,8))[250:]
output_data = output_data - output_data[0]
plt.plot(output_data[:,3])
plt.show()
# %%
