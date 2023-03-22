from django.urls import path
from . import views

# urlpatterns = [
#     #Exp: /polls/
#     path("", views.index, name ="index"),
#     #Exp: /polls/3/
#     path("<int:question_id>/", views.detail, name ="detail"),
#     #Exp: /polls/3/results
#     path("<int:question_id>/result/", views.result, name ="result"),
#     #Exp: /polls/3/vote
#     path("<int:question_id>/vote/", views.vote, name ="vote")
# ]
urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:question_id>", views.detail, name="detail"),
    path("result/<int:question_id>", views.result, name="result"),
    path("vote/<int:question_id>", views.vote, name="vote"),
]