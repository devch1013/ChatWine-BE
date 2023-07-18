from django.shortcuts import HttpResponse
from ai.streaming import streaming
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .apps import WineConfig
import json
# Create your views here.

def test(request):
    print(request)
    return HttpResponse({"hello":"ok"})

@csrf_exempt
def streaming_test(request):
    if request.method == "POST":
        text = body2json(request.body).get("text")
        print(text)
        result = WineConfig.audrey.forward(text)
        # stream = streaming(text)
    else:
        result = WineConfig.audrey.forward("안녕")
        # result = streaming(text="  complete!")
    response = StreamingHttpResponse(result, status=200, content_type='text/event-stream')
    print(response)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def body2json(body):
    data = json.loads(body.decode('utf-8'))
    return data