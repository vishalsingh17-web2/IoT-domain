from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import joblib
import pickle



def index(request):
    try:
        with open('myApp/rnn_fall.pkl', 'rb') as f:
            rnn_fall = pickle.load(f)
        encoder = joblib.load('myApp/rnn_decoder.sav')
        # clf.predict([[1,2,3,4,5,6,7,8,9]])
        return JsonResponse({"status": 'Success'})
    except:
        return JsonResponse({'error': 'Model not found'})
    

@csrf_exempt
def sensorsData(request):
    if request.method == 'POST': 
        received_json_data=json.loads(request.body)
        #Machine learning
        clf = joblib.load('myApp/rnn_fall.sav')
        encoder = joblib.load('myApp/rnn_decoder.sav')
        out = clf.predict(received_json_data.get('data'))
        activity = encoder.inverse_transform(out)
        print(activity)
        
        return JsonResponse({"prediction": activity[0]}) 

    return JsonResponse({"status": 'Error'})