import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf

from keras import layers
from keras import losses

batch_size = 32
seed = 42

#Split training dataset into training and validation set
raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    'main_directory', 
    batch_size=batch_size, 
    validation_split=0.2, 
    subset='training', 
    seed=seed)

#Confirm value of labels
print("Label 0 corresponds to", raw_train_ds.class_names[0])
print("Label 1 corresponds to", raw_train_ds.class_names[1])

#load remaining vaues in dataset
raw_val_ds = tf.keras.utils.text_dataset_from_directory(
    'main_directory', 
    batch_size=batch_size, 
    validation_split=0.2, 
    subset='validation', 
    seed=seed)

#load test values
raw_test_ds = tf.keras.utils.text_dataset_from_directory(
    'test_directory', 
    batch_size=batch_size)

#text vectorization
def custom_standardization(input_data):
  lowercase = tf.strings.lower(input_data)
  stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
  return tf.strings.regex_replace(stripped_html,
                                  '[%s]' % re.escape(string.punctuation),
                                  '')

max_features = 10000
sequence_length = 250

vectorize_layer = layers.TextVectorization(
    standardize=custom_standardization,
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

# Make a text-only dataset (without labels), then call adapt
train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label

text_batch, label_batch = next(iter(raw_train_ds))
first_ngram, first_label = text_batch[0], label_batch[0]
print("Ngram", first_ngram)
print("Label", raw_train_ds.class_names[first_label])
print("Vectorized review", vectorize_text(first_ngram, first_label))

#Cleaning up text with text vectorization
train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

#Preformance boost
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

embedding_dim = 16

model = tf.keras.Sequential([
  layers.Embedding(max_features + 1, embedding_dim),
  layers.Dropout(0.2),
  layers.GlobalAveragePooling1D(),
  layers.Dropout(0.2),
  layers.Dense(1)])

model.summary()


#configuring model to use optimizer and appropriate loss function
model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=tf.metrics.BinaryAccuracy(threshold=0.0))

#Training the model
epochs = 10
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs)

#Evaluating the model
loss, accuracy = model.evaluate(test_ds)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

