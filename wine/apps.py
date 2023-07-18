from django.apps import AppConfig
from ai.chatbot import Audrey

class WineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wine'
    audrey = Audrey()
