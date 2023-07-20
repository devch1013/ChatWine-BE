from django.urls import path, include
from wine.views import first_conversation, conversation, get_user_example


urlpatterns = [
    path("", first_conversation),
    path("<int:conversation_id>", conversation),
    path("example/<int:ex_id>", get_user_example),
]
