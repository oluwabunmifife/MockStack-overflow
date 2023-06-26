from django.urls import path
from .views import question_list, question_details, register, create_question, update_question

urlpatterns = [
    path('question/', question_list, name='qlist'),
    path('question/<slug:slug>/', question_details, name='qdetails'),
    path('register/', register, name='register'),
    path('add/', create_question, name='create_question'),
    path('update/<slug:slug>/', update_question, name='update_question'), # type: ignore
]