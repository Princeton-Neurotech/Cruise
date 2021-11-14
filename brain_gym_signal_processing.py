#%%
import pandas as pd

orig_folder = 'Data'

#Reads CSV file and closes it once information extracted.
def read_txt(filename):
    f = open(filename, "r")
    original = f.readlines()
    f.close()

    final_percentage = 0
    for idx in range(len(original)):
        if original[idx][0] == '%':
            final_percentage = idx + 
        else: break
    original = original[final_percentage:]

    f = open(orig_folder + "/temp.csv", "w")
    f.write(''.join(original))
    f.close()

    return pd.read_csv('temp.csv')

#%%
import os
import pandas as pd
from tqdm import tqdm

#Turns data into labeled rows and columns to make data easier to work with
# col1 = person name
# col2 = alpha/beta/gamma/theta/work
all_people = pd.DataFrame()

people = [folder for folder in os.listdir() if not os.path.isfile(folder)]
for person in tqdm(people):
    current_dir = os.listdir(person)
    for folder in current_dir:
        if folder in {'Alpha', 'Beta', 'Gamma', 'Theta', 'Work'}:
            files = os.listdir(person + '/' +folder)

            # skip folder if more than one file in it (unclear which to choose)
            if len(files) > 1: continue

            path = orig_folder +'/'+ person +'/'+ folder +'/'+ files[0]
            temp_df = read_txt(path)
            temp_df['person'] = person
            temp_df['folder'] = folder

            all_people = all_people.append(temp_df)

#%%
import numpy as np

np_all_people = all_people.to_numpy()
with open('all_people_data_np.npy', 'wb') as f:
    np.save(f, np_all_people)
# %%
