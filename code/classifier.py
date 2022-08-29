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
x3 = numpy.asarray(dataset[:,2:3])
y = numpy.asarray(dataset[:,3])

