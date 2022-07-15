import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

BIGRAMS_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\output\bigrams.txt"
DEPTH = 30

dataframe = open(BIGRAMS_FILE_PATH, "r", encoding="utf-8", errors="replace").read()
x = dataframe[:,0:DEPTH]
y = dataframe[:,DEPTH]

encoder = LabelEncoder()
encoder.fit(y)
encoded_Y = encoder.transform(y)

def sequential_model():
	model = Sequential()
	model.add(Dense(60, input_shape=(DEPTH,), activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

estimator = KerasClassifier(model=sequential_model, epochs=100, batch_size=5, verbose=0)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, x, encoded_Y, cv=kfold)
print(results.mean()*100)