import numpy as np
import pandas as pd
from tensorflow import keras
from keras.layers import BatchNormalization
import tensorflow as tf

dataset = pd.read_csv('Dataset_with_fall.csv')
dataset = dataset.drop(['user','Magnetometer_X','Magnetometer_Y','Magnetometer_Z', 'Gyroscope_X','Gyroscope_Y','Gyroscope_Z'], axis=1)
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
# print(dataset.head())

y_training = np.array(y[0:len(y)-21])
x_training = []
for i in range(len(x)-21):
    x_tr = []
    for j in range(i,i+21):
        for k in range(6):
            x_tr.append(x[j][k])
    x_training.append(x_tr)

from sklearn.preprocessing import OneHotEncoder
HotEncode = OneHotEncoder()
y = HotEncode.fit_transform(y.reshape(9396,1)).toarray()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 3)

# x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size = 0.2, random_state = 1)
x_train = tf.expand_dims(x_train, axis=2)
# x_validation = tf.expand_dims(x_validation, axis=2)
# y_train = tf.expand_dims(y_train, axis=2)
# y_validation = tf.expand_dims(y_validation, axis=2)
x_test = tf.expand_dims(x_test, axis=2)
# y_test = tf.expand_dims(y_test, axis=2)

def build_model():
    model = tf.keras.Sequential()
    activation = 'relu'
    model.add(keras.layers.LSTM(units=128, input_dim=3, input_shape = (x_train.shape[1:]), activation=activation, return_sequences=True))
    model.add(keras.layers.Dropout(0.2))
    model.add(BatchNormalization())
    model.add(keras.layers.LSTM(units=128, activation=activation))
    model.add(keras.layers.Dropout(0.2))
    model.add(BatchNormalization())
    model.add(keras.layers.Dense(units=32, activation=activation))
    model.add(BatchNormalization())
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(units=7, activation='softmax'))
    return model


class myCallback(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if logs.get('val_accuracy') >= 0.92 and logs.get('accuracy') >= 0.98:
                self.model.stop_training = True
                print("\nReached 98% accuracy so cancelling training!") 


callbacks = myCallback()

model = build_model()
model.compile(optimizer=tf.optimizers.Adam(decay=1e-5,learning_rate=1e-3), loss='mse', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=1200, callbacks=[callbacks],validation_data=(x_test, y_test))
print(model.summary())
print(model.evaluate(x_test, y_test))
print(model.metrics_names)

# for i in range(0,15):
#     print(HotEncode.inverse_transform(model.predict(np.array([x_test[i,:]]))))

# print(y_test[0:15,:])

