from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import joblib


def index(request):
    clf = joblib.load('myApp/final.sav')
    encoder = joblib.load('myApp/encoder.sav')
    return JsonResponse({"Happy family": 'Aman, Akshuni & Akshunn'})

@csrf_exempt
def sensorsData(request):
    if request.method == 'POST': 
        received_json_data=json.loads(request.body)
        #Machine learning
        clf = joblib.load('myApp/final.sav')
        encoder = joblib.load('myApp/encoder.sav')
        out = clf.predict(received_json_data.get('data'))
        activity = encoder.inverse_transform(out)
        print(activity)
        
        return JsonResponse({"prediction": activity[0]}) 

    return JsonResponse({"status": 'Error'})