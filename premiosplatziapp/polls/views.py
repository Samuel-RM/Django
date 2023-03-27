from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse ,  HttpResponseRedirect
from django.urls import reverse

from .models import Question , Choice


def index(request):
    lates_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "lates_question_list":lates_question_list
    })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request , "polls/result.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) 
    except (KeyError, Choice.DoesNotExist): 
        return render(request , "polls/datail.html", {
            "question": question,
            "error_message": "NO elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result", args=(question_id,)))