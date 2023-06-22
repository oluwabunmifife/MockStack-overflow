from django.urls import path
from .views import question_list, question_details, register

urlpatterns = [
    path('question/', question_list, name='qlist'),
    path('question/<slug:slug>', question_details, name='qdetails'),
    path('register/', register, name='register'),
]
