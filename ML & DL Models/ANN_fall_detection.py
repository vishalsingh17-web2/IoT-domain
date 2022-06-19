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

y_training = np.array(y[0:len(y)-40])
x_training = []
for i in range(len(x)-40):
    x_tr = []
    for j in range(i,i+40):
        for k in range(6):
            x_tr.append(x[j][k])
    x_training.append(x_tr)

from sklearn.preprocessing import OneHotEncoder
y = OneHotEncoder().fit_transform(y.reshape(y.shape[0],1)).toarray()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)
print(x_train.shape[1])
print(np.array([x_test[100,:]]))

class myCallback(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if logs.get('accuracy') > 0.98 and logs.get('loss') < 0.80:
                print("\nReached 98% accuracy so cancelling training!") 
                self.model.stop_training = True


callbacks = myCallback()
model =  tf.keras.Sequential()
activation = 'sigmoid'
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='uniform', input_dim=x_train.shape[1]))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='uniform'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='uniform'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='uniform'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='uniform'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=7, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=1200, callbacks=[callbacks], batch_size=32, validation_data=(x_test, y_test))

# print(y_test[0:15,:])

# print(dataset["Activity"].unique())
print(model.evaluate(x_test, y_test, batch_size=32))
print(model.metrics_names)
