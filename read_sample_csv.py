#%%
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, iirnotch

orig_folder = 'Data'
input_data = 'Data/example_single_person_single_reading.csv'
data = pd.read_csv(input_data)

# 250Hz update rate, 24x gain
# https://docs.openbci.com/Cyton/CytonDataFormat/
scale = 4.5 / 24 / (2^23 - 1)
eeg_data = data.iloc[1:,1:9]*scale
eeg_data = eeg_data - eeg_data.iloc[0,:] # centre data
eeg_data.iloc[0,:]

# Apply band pass filter to remove unnecessary noise
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter(5, 50, 250, order=order)
    y = lfilter(b, a, data)
    return y

# Apply notch filter to remove electrical noise
fs = 200.0  # Sample frequency (Hz)
f0 = 60.0  # Frequency to be removed from signal (Hz)
Q = 30.0  # Quality factor
b,a = iirnotch(f0, Q, fs)
# bottomfreq = 5
# topfreq = 50

# still some drift to deal with

# plt.plot(data.iloc[1:,12:19])
# plt.show()



#%%
import mne
np_eeg = eeg_data.to_numpy().reshape((8,-1))
output_data = mne.filter.filter_data(data = np_eeg, sfreq = 250, l_freq=10, h_freq=30)

output_data = output_data.reshape((-1,8))
plt.plot(output_data)
plt.show()
# %%
