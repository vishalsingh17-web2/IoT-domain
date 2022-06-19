import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder as le
import joblib

data = pd.read_csv("Dataset.csv")

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
data.dropna()
data['Activity']= le.fit_transform(data['Activity'])
data = data.drop(['Gyroscope_Z','Gyroscope_X','Gyroscope_Y'], axis=1)

ytrain = data.pop("Activity")
ytrain = np.array(ytrain)
data.pop("user")
data.pop("Magnetometer_X")
data.pop("Magnetometer_Y")
data.pop("Magnetometer_Z")
xtrain = data.to_numpy()


x = np.array(xtrain)
y_training = np.array(ytrain[0:len(ytrain)-15])
x_training = []
for i in range(len(x)-15):
    x_tr = []
    for j in range(i,i+15):
        for k in range(6):
            x_tr.append(x[j][k])
    x_training.append(x_tr)
    
# print(len(x_training), len(y_training))
X_train,X_test,y_train,y_test = train_test_split(x_training,y_training,test_size=0.2, random_state=2)

from sklearn.ensemble import RandomForestClassifier
clf=RandomForestClassifier(n_estimators=200)
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)
from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
le.inverse_transform(y_pred)

# joblib.dump(clf, 'final.sav')
# joblib.dump(le, 'encoder.sav')