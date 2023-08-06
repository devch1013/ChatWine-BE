from django.shortcuts import HttpResponse
from ai.streaming import streaming
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .apps import WineConfig
from .models import Conversation, Utterance, ChatExamples, WineData
import json

# Create your views here.


def test(request):
    print(WineData.objects.all()[:10])
    return "hello"


@csrf_exempt
def first_conversation(request):
    conv = Conversation()
    conv.save()
    return conversation(request, conv.id)


@csrf_exempt
def conversation(request, conversation_id):
    if request.method == "POST":
        
        conversation = Conversation.objects.get(id=conversation_id)
        print(conversation.id)

        text = body2json(request.body).get("text")
        print("="*30)
        print('conversation_id', conversation_id)
        print('text', text)
        print('conversation object', conversation.stage_history)
        print('chat_history', get_chat_history(conversation))
        print("stage_history", conversation.stage_history)
        print("="*30)
        result = WineConfig.audrey.forward(
            text,
            conversation_object=conversation,
            chat_history=get_chat_history(conversation),
        )
        # stream = streaming(text)
        response = StreamingHttpResponse(result, status=200, content_type="text/event-stream")
        # print(response)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        print('response', response)
        return response
    # else:
    #     result = WineConfig.audrey.forward("안녕")
    # result = streaming(text="  complete!")
    return HttpResponse("")


def body2json(body):
    data = json.loads(body.decode("utf-8"))
    return data


def get_chat_history(obj):
    utters = Utterance.objects.all().filter(conversation=obj).order_by("-timestamp")
    chat_hist = ""
    for utter in utters[:2:-1]:
        chat_hist += "User: " + utter.user_side + "<END_OF_TURN>"
        chat_hist += "이우선: " + utter.ai_side + "<END_OF_TURN>"
    print('chat_hist', chat_hist)
    return chat_hist


def get_user_example(request, ex_id):
    qs = ChatExamples.objects.get(id=ex_id)
    return HttpResponse(qs.example)
