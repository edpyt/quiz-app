from django.urls import path

from . import api


urlpatterns = [
    path('all/', api.quiz_list, name='quiz_list'),
    path('<uuid:pk>/', api.quiz_detail, name='quiz_detail'),
    path('quiz_answer/', api.quiz_answer, name='quiz_answer'),
]