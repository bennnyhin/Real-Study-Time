import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

def plottimes(times, ID):
    times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
    sns.scatterplot(data=times, x="Expected time", y="Actual time");
    #plt.show()
    plt.savefig(f'{ID}.png')

plottimes(np.random.rand(200, 2)*60)