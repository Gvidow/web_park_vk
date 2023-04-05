from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import get_questions, get_user, get_question, get_answers, log_out, log_in
from .models import question_by_tag
from .models import TAGS, MEMBERS, AUTHORIZED
from random import choice


def index(request):
    context = {"questions": get_questions(), "user_data": get_user(AUTHORIZED.status),
               "tags": TAGS, "best_members": MEMBERS}
    return render(request, "index.html", context)


def question(request, id):
    context = {
        "question": get_question(id),
        "user_data": get_user(AUTHORIZED.status),
        "answers": get_answers(id),
        "tags": TAGS, "best_members": MEMBERS,
    }
    return render(request, "question.html", context)


def setting(request, id):
    context = {
        "user_data": get_user(id),
        "user": None,
        "tags": TAGS, "best_members": MEMBERS,
    }
    return render(request, "settings.html", context)


def logout(request):
    log_out()
    return HttpResponseRedirect('/')


def login(request):
    log_in()
    context = {"tags": TAGS, "best_members": MEMBERS}
    return render(request, "login.html", context)


def signup(request):
    context = {"tags": TAGS, "best_members": MEMBERS}
    return render(request, "register.html", context)


def search_by_tag(request, tag):
    context = {
        "questions": question_by_tag(tag),
        "tag": tag,
        "tags": TAGS,
        "best_members": MEMBERS,
    }
    return render(request, "tag.html", context)
