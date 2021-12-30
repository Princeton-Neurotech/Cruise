# import pyedflib
# import numpy as np

# file_name = pyedflib.data.get_generator_filename()
# f = pyedflib.EdfReader(file_name)
# n = f.signals_in_file
# signal_labels = f.getSignalLabels()
# sigbufs = np.zeros((n, f.getNSamples()[0]))
# for i in np.arange(n):
#         sigbufs[i, :] = f.readSignal(i)


# from pyedflib import highlevel

# signals, signal_headers, header = highlevel.read_edf('person1alphatest.edf')
# eeg_data = signals[1:1+8].reshape(-1,8)

import mne
import numpy as np

raw = mne.io.read_raw_edf('person1alphatest.edf')
