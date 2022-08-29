#Used for loading the csv data
from telnetlib import X3PAD
import pandas
import numpy

#Model architecture
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils

#Used for data preparation and model evaluation
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

BIGRAMS_FILE_PATH = r"bigrams.csv"

dataframe = pandas.read_csv(BIGRAMS_FILE_PATH, header=None)
dataset = dataframe.values

x1 = numpy.asarray(dataset[:,0:1])
x2 = numpy.asarray(dataset[:,1:2])
y = numpy.asarray(dataset[:,2])

x1_train, x1_test, x2_train, x2_test, y_train, y_test = train_test_split(x1, x2, y, test_size=0.2)

svc = SVC()
svc.fit(x1_train, x2_train, y_train)
score = svc.score(x1_train, x2_train, y_train)

cross_val = cross_val_score(svc, x1_train, x2_train, y_train, cv=10)

y_pred = svc.predict(x1_test, x2_test)
con_matrix = confusion_matrix(y_test, y_pred)
classification = classification_report(y_test, y_pred)

print(y_pred, con_matrix, classification)