from sklearn import svm
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_noisy_data(): #Generate noisy data for testing
    X = np.sort(5 * np.random.rand(200, 1), axis=0)
    y = np.sin(X).ravel()
    y[::5] += 3 * (0.5 - np.random.rand(40))

    times = np.column_stack((X, y))
    return times

def train(times, ID, x): # Times is tuple or iterable in same format as generate_noisy_data (dimensions are (x, 2)). Saves model to ID.pkl
    times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
    regr = svm.SVR()
    regr.fit(times["Expected time"].values.reshape(-1, 1), times["Actual time"].values.reshape(-1, 1))
    with open(f'{ID}.pkl', 'wb') as fid:
        pickle.dump(regr, fid)
    return regr.predict(np.asarray(x).reshape(1, -1))

def predict(x, ID): # Predict from saved model named ID.pkl. x is a float. Training is so fast that this shouldn't be necessary, but it's here anyways. 
    with open(f'{ID}.pkl', 'rb') as fid:
        regr_loaded = pickle.load(fid)
    return regr_loaded.predict(np.asarray(x).reshape(1, -1))

#EXAMPLE IMAGE CALLED plotmodel.png
def plotmodel(times, ID): # plot model from past times, same format as train and generate_noisy_data
    times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
    X = times["Expected time"].values.reshape(-1, 1)
    y = times["Actual time"].values.reshape(-1, 1)
    svr = svm.SVR(gamma=0.1, epsilon=.1)
    fig, axes = plt.subplots(figsize=(15, 10))
    axes.plot(X, svr.fit(X, y).predict(X), color="g", lw=2,
                label='{} model'.format("SVM regression"))
    axes.scatter(X[svr.support_], y[svr.support_], facecolor="none",
                    edgecolor="g", s=50,
                    label='{} support vectors'.format("SVM Regression"))
    axes.scatter(X[np.setdiff1d(np.arange(len(X)), svr.support_)],
                    y[np.setdiff1d(np.arange(len(X)), svr.support_)],
                    facecolor="none", edgecolor="k", s=50,
                    label='other training data')
    axes.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
                    ncol=1, fancybox=True, shadow=True)

    fig.text(0.5, 0.04, 'Expected time', ha='center', va='center')
    fig.text(0.06, 0.5, 'Actual time', ha='center', va='center', rotation='vertical')
    fig.suptitle("Support Vector Regression", fontsize=14)
    #plt.show()
    plt.savefig(f'{ID}model.png')

#EXAMPLE IMAGE CALLED plottimes.png
def plottimes(times, ID): # plot times only
    sns.set_theme(style="whitegrid")
    times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
    sns.scatterplot(data=times, x="Expected time", y="Actual time");
    #plt.show() # uncomment to see the plot yourself
    plt.savefig(f'{ID}.png')
