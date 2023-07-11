from django.shortcuts import render, HttpResponse
from ai.streaming import streaming
from django.http.response import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
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
        stream = streaming(text)
    else:
        stream = streaming(text="  complete!")
    response = StreamingHttpResponse(stream, status=200)
    response['Cache-Control'] = 'no-cache'
    return response


def body2json(body):
    data = json.loads(body.decode('utf-8'))
    return data