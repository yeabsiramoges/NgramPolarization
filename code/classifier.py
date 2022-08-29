#Used for loading the csv data
import pandas
import numpy

#Model architecture
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils

#Used for data preparation and model evaluation
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

BIGRAMS_FILE_PATH = r"bigrams.csv"

dataframe = pandas.read_csv(BIGRAMS_FILE_PATH, header=None)
dataset = dataframe.values

X = numpy.asarray(dataset[:,0:3])
Y = numpy.asarray(dataset[:,3])

encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)

test_Y = numpy.asarray(np_utils.to_categorical(encoded_Y))

def model():
    model = Sequential()
    model.add(Dense(8, input_dim=4, activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

estimator = KerasClassifier(build_fn=model, epochs=200, batch_size=5, verbose=0)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_predict(estimator, X, test_Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))