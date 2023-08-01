from django.urls import path
from .views import Hello

urlpatterns = [
    path("hi", Hello.as_view())
]