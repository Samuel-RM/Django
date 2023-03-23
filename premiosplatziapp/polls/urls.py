from django.urls import path
from . import views

urlpatterns = [
    #ex: /polls/
    path('', views.index, name='index'),
    #ex: /polls/5
    path('<int:question_id>/', views.detail, name='detail'),
    #ex: /polls/5/results
    path('<int:question_id>/result/', views.result, name='results'),
    #ex: /polls/5/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
# urlpatterns = [
#     path("", views.index, name="index"),
#     path("detail/<int:question_id>", views.detail, name="detail"),
#     path("result/<int:question_id>", views.result, name="result"),
#     path("vote/<int:question_id>", views.vote, name="vote"),
# ]