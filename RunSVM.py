__author__ = 'phantom'
import numpy as np
from sklearn import svm

def preprocess():
    n_features = 14
    n_sample = 5000
    train_data = np.zeros((n_sample, n_features+1), dtype=np.int)
    f = open("matrix_info.txt", "r")
    row_index = 0
    for line in f:
        row_data=line.split("|")
        column_index = 0
        for data in row_data:
            train_data[row_index][column_index] = data
            column_index += 1
        row_index += 1
    f.close()
    train_label = train_data[:, n_features:]
    train_data = train_data[:, 0:n_features]
    return train_data, train_label

train_data, train_label = preprocess()
print train_data.shape
print train_label.shape

train_label = train_label.ravel()

#Radial basis function , gamma = 1.0
print('\n--------Radial basis function , Gamma Default-------------------')
clf = svm.SVC(kernel='rbf', gamma=0.0);
clf.fit(train_data, train_label);
predicted_label = clf.predict(train_data);
print('\n Radial basis function Gamma default Train set Accuracy:' + str(100*np.mean((predicted_label == train_label).astype(float))) + '%');
