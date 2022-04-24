from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import joblib
import pickle
from tensorflow import keras
import math

def tilt(acc_data):
    
    norm_Of_g = math.sqrt(acc_data[0]**2 + acc_data[1]**2 + acc_data[2]**2)
    acc_data[0] = acc_data[0] / norm_Of_g
    acc_data[1] = acc_data[1] / norm_Of_g
    acc_data[2] = acc_data[2] / norm_Of_g
    # print(acc_data[2])
    inclination = math.degrees(math.acos(acc_data[2]))
    # print(inclination)
    return inclination

def process_batch(acc_batch):
    acc_data = []
    for i in range(0,40):
        acc_data.append(acc_batch[3*i:3*i+3])
    status = 0
    standing = 0
    for i in acc_data:
        angle = tilt(i)
        if(angle<25 or angle>155):
            status-=1
        else:
            status+=1
        if(angle>75 and angle<105):
            standing-=1
        else:
            standing+=1

    return status,standing


def index(request):
    try:
        # with open('myApp/rnn_fall.h5', 'rb') as f:
        rnn_fall = joblib.load('myApp/final.sav')
        encoder = joblib.load('myApp/encoder.sav')
        # clf.predict([[1,2,3,4,5,6,7,8,9]])
        return JsonResponse({"status": 'Success'})
    except:
        return JsonResponse({'error': 'Model not found'})
    

@csrf_exempt
def sensorsData(request):
    if request.method == 'POST': 
        data=json.loads(request.body)
        #Machine learning
        
        model_data = data.get('data')
        accel = data.get('accel')
        val,standing = process_batch(accel)

        # print(accel)
        # print(len(accel))
        # print(len(data))
        # for i in range(9):
        #     data[0][i] = float(data[0][i])
        # clf = keras.models.load_model('myApp/rnn_fall_model.h5')
        # out = clf.predict(data)
        # encoder = joblib.load('myApp/rnn_fall_encoder.sav')
        # activity = encoder.inverse_transform(out)

        model = joblib.load('myApp/final.sav')
        encoder = joblib.load('myApp/encoder.sav')
        out = model.predict([model_data])
        activity = encoder.inverse_transform(out)
        
        if(val>0 and standing>0):
            print(activity[0], "1st case")
            return JsonResponse({"prediction": activity[0]})
        elif(val<=0 and activity[0]=="Fall"):
            print("idle")
            if(standing<=0):
                return JsonResponse({"prediction": "Standing"})
            return JsonResponse({"prediction":"Idle"})
        elif(val>0 and standing<=0 and activity[0]=="Fall"):
            print("Standing")
            return JsonResponse({"prediction": "Standing"})
        elif(val<=0 and standing>0 and activity[0]=="Fall"):
            print(activity[0])
            return JsonResponse({"prediction": "Idle"})        
        else:
            print(activity[0],"else case")
            return JsonResponse({"prediction": activity[0]})

        
        
    return JsonResponse({"status": 'Error'})