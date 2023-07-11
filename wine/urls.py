
from django.urls import path, include
from wine.views import test, streaming_test


urlpatterns = [
    path("", streaming_test)
]
