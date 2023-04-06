from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import get_questions, get_user, get_question, get_answers, log_out, log_in
from .models import question_by_tag
from .models import TAGS, MEMBERS, AUTHORIZED


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@csrf_exempt
def index(request):
    questions = get_questions()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(AUTHORIZED.status),
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "index.html", context)


@csrf_exempt
def question(request, id):
    q = get_question(id)
    if q is None:
        return HttpResponseNotFound()
    context = {
        "question": q,
        "user_data": get_user(AUTHORIZED.status),
        "answers": get_answers(id),
        "tags": TAGS, "best_members": MEMBERS,
    }
    return render(request, "question.html", context)


@csrf_exempt
def setting(request, id):
    user = get_user(id)
    if user is None:
        return HttpResponseNotFound()
    context = {
        "user_data": user,
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
        "page_obj": paginate(question_by_tag(tag), request),
        "tag": tag,
        "tags": TAGS,
        "best_members": MEMBERS,
    }
    return render(request, "tag.html", context)


def ask(request):
    context = {"tags": TAGS, "best_members": MEMBERS}
    return render(request, "ask.html", context)
