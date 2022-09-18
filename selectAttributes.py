# from sklearn.datasets import load_wine
# from sklearn.feature_selection import RFE
# from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.utils import Bunch
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import csv
from loadDataset import *
import pandas as pd
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
X = file.data
y = file.target
feature_names = file.feature_names


# SELECT K ATTRIBUTES
KBest = SelectKBest(chi2, k=100)

X_new = KBest.fit_transform(X, y)
column_names = [column[0]
                for column in zip(file.feature_names, KBest.get_support()) if column[1]]


# Separando treinamento e teste

X_train, X_val, y_train, y_val = train_test_split(
    X_new, y, test_size=0.2, random_state=1)


# APPLY NAIVE BAYERS
nb = GaussianNB()
nb.fit(X_train, y_train)

y_pred = nb.predict(X_val)
print(nb.score(X_val, y_val))
resp = pd.DataFrame({"Atual": y_val, "Previsao": y_pred})
print(resp)
