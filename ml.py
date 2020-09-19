from sklearn import svm
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_noisy_data(): #Generate noisy data for testing
    X = np.sort(5 * np.random.rand(200, 1), axis=0)
    y = X.ravel()
    y = np.random.normal(y, .2)

    times = np.column_stack((X, y+0.1))
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
def plotmodel(times, ID, percentage=False, model=True): # plot model from past times, same format as train and generate_noisy_data
    times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
    X = times["Expected time"].values.reshape(-1, 1)
    y = times["Actual time"].values.reshape(-1, 1)
    svr = svm.SVR(gamma=0.1, epsilon=.1)
    fig, axes = plt.subplots(figsize=(15, 10))
    if percentage:
        if max(X/y)<0.9 and min(X/y)>-0.9:
            axes.set_ylim([-1, 1])
        else:
            axes.set_ylim([min(y/X)-0.1, max(y/X)+0.1])
        y_plt = y/X
        fig.text(0.5, 0.04, 'Expected time', ha='center', va='center')
        fig.text(0.06, 0.5, 'Actual time / Expected time (lower is better)', ha='center', va='center', rotation='vertical')
    else:
        axes.set_ylim([1.5*min(X-y), 1.5*max(X-y)])
        y_plt = X-y
        fig.text(0.5, 0.04, 'Expected time', ha='center', va='center')
        fig.text(0.06, 0.5, 'Expected time - Actual time (lower is better)', ha='center', va='center', rotation='vertical')
    if model:
        axes.plot(X, (svr.fit(X, y_plt).predict(X)), color="g", lw=2,
                label='{} model'.format("SVM regression"))
    axes.scatter([i for idx,i in enumerate(X) if X[idx]<y[idx]], [i for idx,i in enumerate(y_plt) if X[idx]<y[idx]], facecolor="none",
                    edgecolor="g" if percentage is not True else "r", s=50,
                    label='Shorter than expected')
    axes.scatter([i for idx,i in enumerate(X) if X[idx]>y[idx]],[i for idx,i in enumerate(y_plt) if X[idx]>y[idx]],
                    facecolor="none", edgecolor="r" if percentage is not True else "g" , s=50,
                    label='Longer than expected')
    axes.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
                    ncol=1, fancybox=True, shadow=True)
    
    fig.suptitle("Support Vector Regression", fontsize=14)
    #plt.show()
    plt.savefig(f'{ID}.png')

#plotmodel(generate_noisy_data(), 1, percentage=True)