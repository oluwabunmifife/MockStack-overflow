from django.urls import path
from .views import question_list, question_details, register, create_question, update_question, delete_question, update_answer, delete_answer, change_profile, list_info

urlpatterns = [
    path('question/', question_list, name='qlist'),
    path('question/<slug:slug>/', question_details, name='qdetails'),
    path('register/', register, name='register'),
    path('add/', create_question, name='create_question'),
    path('update/<slug:slug>/', update_question, name='update_question'), # type: ignore
    path('delete/<slug:slug>/', delete_question, name='delete_question'),
    path('answer/update/<int:id>/', update_answer, name='update_answer'),
    path('answer/delete/<int:id>/', delete_answer, name='delete_answer'),
    path('profile/', change_profile, name='change_profile'),
    path('list/', list_info, name='list_info'),
]