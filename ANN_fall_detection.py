import numpy as np
import pandas as pd
from tensorflow import keras
from keras.layers import BatchNormalization
import tensorflow as tf
from sklearn.metrics import confusion_matrix, accuracy_score

dataset = pd.read_csv('Dataset.csv')
dataset = dataset.drop(['user','Magnetometer_X','Magnetometer_Y','Magnetometer_Z'], axis=1)
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
# print(dataset.head())

from sklearn.preprocessing import OneHotEncoder
y = OneHotEncoder().fit_transform(y.reshape(9396,1)).toarray()

# For reference:
# print(y[8347,:]) #standing - [0 0 1 0 0 0]
# print(y[7623,:]) #walking upstairs - [0 0 0 0 0 1]
# print(y[7013,:]) #walking - [0 0 0 1 0 0]
# print(y[4848,:]) #walking downstairs - [0 0 0 0 1 0]
# print(y[3889,:]) #sitting - [0 1 0 0 0 0]
# print(y[1506,:]) #brisk walking - [1 0 0 0 0 0]


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)
print(x_train.shape[1])
print(np.array([x_test[100,:]]))

class myCallback(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if logs.get('accuracy') > 0.985 and logs.get('loss') < 0.80:
                print("\nReached 98% accuracy so cancelling training!") 
                self.model.stop_training = True


callbacks = myCallback()
model =  tf.keras.Sequential()
activation = 'relu'
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='random_normal', input_dim=x_train.shape[1]))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='random_normal'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='random_normal'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='random_normal'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=32, activation=activation, kernel_initializer='random_normal'))
model.add(BatchNormalization())
model.add(keras.layers.Dense(units=7, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=1200, callbacks=[callbacks], batch_size=64)

acc = history.history["accuracy"]
print(max(acc),acc.index(max(acc)))
import matplotlib.pyplot as plt
xpoints = np.array([i for i in range(len(acc))])
ypoints = np.array(acc)
plt.plot(xpoints, ypoints)
plt.show()

loss = history.history["loss"]
yloss = np.array(loss)
plt.plot(xpoints,yloss)
plt.show()

# for i in range(0,15):
#     if model.predict(np.array([x_test[i,:]])).argmax() == 0:
#         print("brisk walking")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 1:
#         print("sitting")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 2:
#         print("standing")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 3:
#         print("walking")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 4:
#         print("walking down stairs")
#     elif model.predict(np.array([x_test[i,:]])).argmax() == 5:
#         print("walking up stairs")

# print(y_test[0:15,:])

# print(dataset["Activity"].unique())
print(model.evaluate(x_test, y_test, batch_size=32))
print(model.metrics_names)

