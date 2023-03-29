from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    #ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    #ex: /polls/5
    path('<int:pk>/detail/dasdad', views.DetailView.as_view(), name='detail'),
    #ex: /polls/5/results
    path('<int:pk>/result/', views.ResultlView.as_view(), name='result'),
    #ex: /polls/5/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]


# urlpatterns = [
#     path("", views.index, name="index"),
#     path("detail/<int:question_id>", views.detail, name="detail"),
#     path("result/<int:question_id>", views.result, name="result"),
#     path("vote/<int:question_id>", views.vote, name="vote"),
# ]