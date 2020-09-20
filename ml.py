from sklearn import svm
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_noisy_data(): 
    #Generate linear noisy data for testing. 
    X = np.sort(5 * np.random.rand(200, 1), axis=0)
    y = X.ravel()
    y = np.random.normal(y, .1)

    times = np.column_stack((X, y+0.1))
    return times

def train(times, ID, x):
    r'''
    Train and save model:
    args:
    times (iterable): Same format as generate_noisy_data (dimensions are (x, 2))
    ID (str or int): Unique identifier, name of saved model
    x (float): x value (expected time) to predict the y value (actual time)
    '''
    times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
    regr = svm.SVR()
    regr.fit(times["Expected time"].values.reshape(-1, 1), times["Actual time"].values.reshape(-1, 1))
    with open(f'static/{ID}.pkl', 'wb') as fid:
        pickle.dump(regr, fid)
    return regr.predict(np.asarray(x).reshape(1, -1))

def predict(x, ID): 
    r'''
    Predict from a saved model. Training is so fast that this shouldn't be necessary, but it's here anyways. 
    args:
    x (float): x value (expected time) to predict the y value (actual time)
    ID (str or int): Unique identifier, name of input model file
    '''
    with open(f'static/{ID}.pkl', 'rb') as fid:
        regr_loaded = pickle.load(fid)
    return regr_loaded.predict(np.asarray(x).reshape(1, -1))

#EXAMPLE IMAGE CALLED 1.png
def plotmodel(times, ID, percentage=False, model=True): # plot model from past times, same format as train and generate_noisy_data
    r'''
    Function for plotting. Example image produced with this function is titled 1.png.
    args:
    times (iterable): Same format as generate_noisy_data (dimensions are (x, 2))
    ID (int or str): Unique identifier, name of the output image
    percentage (bool): If true, return graph with percentages (y/x). If false, returns difference (x-y)
    model (bool): If true, include line of best fit from model. If false, exclude line of best fit.
    '''
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
        plt.axhline(1, color='black')
    else:
        axes.set_ylim([1.5*min(X-y), 1.5*max(X-y)])
        y_plt = X-y
        fig.text(0.5, 0.04, 'Expected time', ha='center', va='center')
        fig.text(0.06, 0.5, 'Expected time - Actual time (lower is better)', ha='center', va='center', rotation='vertical')
        plt.axhline(0, color='black')
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
    plt.savefig(f'static/{ID}.png')

def stats(times):
    r'''
    Returns statistics about times
    args:
    times (iterable): Same format as generate_noisy_data (dimensions are (x, 2))
    returns dict of:
    average expected time: average of all x (expected time) values
    average actual time: average of all y (actual time) values
    average time difference: average of y-x
    average minutes over: average of y-x (time difference) when y>x (actual takes longer than expected)
    average minutes under: average of y-x (time difference) when y<x (actual takes shorter than expected)
    '''
    X = times[:, 0]
    y = times[:, 1]

    average_expected_time = np.mean(X)
    average_actual_time = np.mean(y)
    
    average_time_difference = np.mean(y-X) # if positive, expected time is smaller than actual.
    average_minutes_over = np.mean(y[np.where(y>X)]-X[np.where(y>X)])
    average_minutes_under = np.mean(y[np.where(y<X)]-X[np.where(y<X)])
    return {"average expected time": average_expected_time, "average actual time": average_actual_time, "time difference": average_time_difference, "average minutes over": average_minutes_over, "average minutes under": average_minutes_under}


#plotmodel(generate_noisy_data(), 1, percentage=False)
#print(stats(generate_noisy_data()))