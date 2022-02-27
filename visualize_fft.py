import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np

# read from csv
df = pd.read_csv("brain.csv")

# identify channel of interest
channel = 3

# filter out fft data of interest
filter_col = [col for col in df if col.startswith('freq') and col.endswith("_" + str(channel))]
df = df[filter_col]

# define x axis
xs = []
for col in df:
    xs.append(int(col.removeprefix("freq_").removesuffix("_" + str(channel))))

# This function is called periodically from FuncAnimation
def animate(i):
    ax.clear()
    data = df.iloc[i]
    ax.plot(xs, data)

# create figure
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, frames=len(df), interval = 500, repeat = False)
plt.show()