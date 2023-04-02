from django.shortcuts import render
from .models import get_questions, get_user
from random import choice


def index(request):
    is_authorized = choice([True, False])
    context = {"questions": get_questions, "user_data": get_user(is_authorized)}
    return render(request, "index.html", context)


def question(request, id):
    is_authorized = choice([True, False])
    context = {
        "question_id": id,
        "user_data": get_user(is_authorized),
    }
    return render(request, "question.html", context)
