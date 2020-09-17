from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.QuizListView.as_view(),name="quiz_list"),
    path('check-correct/<str:slug>/<int:ques_no>/',views.check_correct,name="check_correct"),
    path('submit/<str:slug>/',views.submit,name="submit"),
    path('<str:slug>/<int:ques_no>/',views.start_quiz,name="start_quiz"),
]