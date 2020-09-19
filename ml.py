from sklearn import svm
import pickle
import numpy as np
import pandas as pd

def train(times, ID, x):
    times = pd.DataFrame(times, columns=["Expected time", "Actual time"])
    regr = svm.SVR()
    regr.fit(times["Expected time"].values.reshape(-1, 1), times["Actual time"].values.reshape(-1, 1))
    with open(f'{ID}.pkl', 'wb') as fid:
        pickle.dump(regr, fid)
    return regr.predict(np.asarray(x).reshape(1, -1))

def predict(x, ID):
    with open(f'{ID}.pkl', 'rb') as fid:
        regr_loaded = pickle.load(fid)
    return regr_loaded.predict(np.asarray(x).reshape(1, -1))

print(train(np.random.rand(200, 2)*60, 1, 24))
print(predict(24, 1))