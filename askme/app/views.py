from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import auth, redirects
from django.db.models import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Question, Tag, Answer, Profile
from .models import AUTHORIZED, log_in, log_out, get_user


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@csrf_exempt
def index(request):
    questions = Question.objects.get_questions_all()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),
               "tags": TAGS,
               "best_members": MEMBERS,
               }
    return render(request, "index.html", context)


@csrf_exempt
def question(request, id):
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    try:
        question = Question.objects.get_by_id(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    answers = question.answers.all()
    context = {
        "question": question,
        "user_data": get_user(),
        "answers": answers,
        "tags": TAGS, "best_members": MEMBERS,
    }
    return render(request, "question.html", context)


@csrf_exempt
def setting(request, id):
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    user = get_user()
    if user is None:
        return HttpResponseNotFound()
    context = {
        "user_data": user,
        "tags": TAGS, "best_members": MEMBERS,
    }
    return render(request, "settings.html", context)


def logout(request):
    log_out()
    return HttpResponseRedirect('/')


def login(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = auth.authenticate(request, request.POST)
        if user:
            login(request, user)
            return redirects(reverse('index'),)


    return render(request, "login.html")



    log_in()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS,
        "best_members": MEMBERS,
    }
    return render(request, "login.html", context)


def signup(request):
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"tags": TAGS, "best_members": MEMBERS}
    return render(request, "register.html", context)


def search_by_tag(request, tag: str):
    try:
        questions = Question.objects.by_tag(tag)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),
               "tag": tag,
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "tag.html", context)


def ask(request):
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "user_data": get_user(),
        "tags": TAGS,
        "best_members": MEMBERS
    }
    return render(request, "ask.html", context)


def hot(request):
    questions = Question.objects.hot_questions()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "hot.html", context)


def best_users(request, id: int):
    try:
        profile = Profile.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    questions = profile.questions.all()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "index.html", context)
