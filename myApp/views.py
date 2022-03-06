from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return JsonResponse({"status": 'Success'})

@csrf_exempt
def sensorsData(request):
    if request.method == 'POST': 
        received_json_data=json.loads(request.body)
        print(len(received_json_data.get('data')))
        
        return JsonResponse({"status": 'Success'}) 
    return JsonResponse({"status": 'Error'})