# from sklearn.datasets import load_wine
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier
import csv
from loadDataset import *
import pandas as pd
from sklearn.utils import Bunch
import numpy as np


def load_my_fancy_dataset():
    with open(r'table.csv') as csv_file:
        data_reader = csv.reader(csv_file)
        feature_names = next(data_reader)[:-1]
        data = []
        target = []
        print("Start iterate file")
        for row in data_reader:
            features = row[:-1]
            label = row[-1]
            data.append([float(num) for num in features])
            target.append(int(label))

        print("Finish iterate file ")
        data = np.array(data)
        target = np.array(target)
    print("Finish pack data")
    return Bunch(data=data, target=target, feature_names=feature_names)


file = load_my_fancy_dataset()
# print(file.y)
X = file.data
y = file.target
clf = DecisionTreeClassifier(max_leaf_nodes=10, random_state=0)
print("Start selecting features")
feature_selection = RFE(clf, n_features_to_select=200, step=1)
print("Starting...")
fs = feature_selection.fit(X, y)
print(fs.support_)
print(fs.ranking_)
for i in range(X.shape[1]):
    print('Column: %d, Selected %s, Rank: %.3f' %
          (i, fs.support_[i], fs.ranking_[i]))
