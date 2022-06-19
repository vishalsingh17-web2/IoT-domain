import numpy as np
import pandas as pd
from tensorflow import keras
from keras.layers import BatchNormalization
import tensorflow as tf
from keras import Sequential
import joblib
from keras.layers import LSTM as lstt


dataset = pd.read_csv('Dataset.csv')
dataset = dataset.drop(['user','Magnetometer_X','Magnetometer_Y','Magnetometer_Z'], axis=1)
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
# print(dataset.head())

# x_training = []
# for i in range(len(x)-40):
#     x_tr = []
#     for j in range(i,i+40):
#         for k in range(9):
#             x_tr.append(x[j][k])
#     x_training.append(x_tr)

from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
y = encoder.fit_transform(y.reshape(9396,1)).toarray()





from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 1)
# x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size = 0.2, random_state = 1)
x_train = tf.expand_dims(x_train, axis=2)
# x_validation = tf.expand_dims(x_validation, axis=2)
# y_train = tf.expand_dims(y_train, axis=2)
# y_validation = tf.expand_dims(y_validation, axis=2)
x_test = tf.expand_dims(x_test, axis=2)
# y_test = tf.expand_dims(y_test, axis=2)


model = Sequential()
activation = 'relu'
model.add(lstt(units=128, input_dim=3, input_shape = (x_train.shape[1:]), activation=activation, return_sequences=True))
model.add(keras.layers.Dropout(0.2))
model.add(BatchNormalization())
model.add(keras.layers.LSTM(units=128, activation=activation))
model.add(keras.layers.Dropout(0.2))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation))
model.add(BatchNormalization())
model.add(keras.layers.Dropout(0.3))
model.add(keras.layers.Dense(units=7, activation='softmax'))
    


class myCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('val_accuracy') >= 0.92 and logs.get('accuracy') >= 0.98:
            print("\nReached 98% accuracy so cancelling training!") 
            self.model.stop_training = True


callbacks = myCallback()
model.compile(optimizer=tf.optimizers.Adam(), loss='mse', metrics=['accuracy'])
edit = model.fit(x_train, y_train, epochs=1200, callbacks=[callbacks],validation_data=(x_test, y_test))
y_pred=model.predict(x_test)
from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

print("Confusion matrix:\n",metrics.confusion_matrix(y_test,y_pred))
# model.save('rnn_fall_model.h5')
# joblib.dump(encoder, 'rnn_fall_encoder.sav')

# brisk walking: [0,1,0,0,0,0,0]
# falling: [1,0,0,0,0,0,0]
# sitting: [0,0,1,0,0,0,0]
# standing: [0,0,0,1,0,0,0]
# walking: [0,0,0,0,1,0,0]
# walking upstairs: [0,0,0,0,0,0,1]
# walking downstairs: [0,0,0,0,0,1,0]
# for i in range(0,15):
#     if model.predict(np.array([x_test[i,:]])).argmax() == 1:
#         print("brisk walking")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 2:
#         print("sitting")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 3:
#         print("standing")                                                               
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 4:
#         print("walking")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 5:
#         print("walking down stairs")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 6:
#         print("walking up stairs")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 0:
#         print("falling")

# print(y_test[0:15,:])
