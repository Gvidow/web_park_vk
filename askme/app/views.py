from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Question, Tag, Answer, Profile
from .models import AUTHORIZED, log_in, log_out, get_user
# from .models import get_questions, get_user, get_question, get_answers, log_out, log_in
# from .models import question_by_tag
# from .models import TAGS, MEMBERS, AUTHORIZED


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@csrf_exempt
def index(request):
    questions = Question.objects.all()
    questions = [(question, Question.objects.count_answer(question), Profile.objects.count_like(question.author)) for question in questions]
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "index.html", context)


@csrf_exempt
def question(request, id):
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    try:
        question = Question.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    answers = Answer.objects.answers_to_question(id)
    answers = [(answer, Profile.objects.count_like(answer.author)) for answer in answers]
    context = {
        "question": question,
        "count_like": Profile.objects.count_like(question.author),
        "user_data": get_user(),#AUTHORIZED.status)
        "answers": answers,
        "tags": TAGS, "best_members": MEMBERS,
    }
    return render(request, "question.html", context)


@csrf_exempt
def setting(request, id):
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    user = get_user()#AUTHORIZED.status)
    if user is None:
        return HttpResponseNotFound()
    context = {
        "user_data": user,
        # "user": None,
        "tags": TAGS, "best_members": MEMBERS,
    }
    return render(request, "settings.html", context)


def logout(request):
    log_out()
    return HttpResponseRedirect('/')


def login(request):
    log_in()
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS,
        "best_members": MEMBERS,
    }
    return render(request, "login.html", context)


def signup(request):
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    context = {"tags": TAGS, "best_members": MEMBERS}
    return render(request, "register.html", context)


def search_by_tag(request, tag):
    questions = Question.objects.by_tag(tag)
    questions = [(question, Question.objects.count_answer(question), Profile.objects.count_like(question.author)) for
                 question in questions]
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),
               "tag": tag,
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "tag.html", context)


def ask(request):
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    context = {
        "user_data": get_user(),
        "tags": TAGS,
        "best_members": MEMBERS
    }
    return render(request, "ask.html", context)

def hot(request):
    questions = Question.objects.hot_questions()
    questions = [(question, Question.objects.count_answer(question), Profile.objects.count_like(question.author)) for
                 question in questions]
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "hot.html", context)

def best_users(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    questions = Question.objects.filter(author=profile)
    questions = [(question, Question.objects.count_answer(question), Profile.objects.count_like(question.author)) for
                 question in questions]
    TAGS = Tag.objects.all()
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "user_data": get_user(),  # AUTHORIZED.status)
               "tags": TAGS, "best_members": MEMBERS,
               }
    return render(request, "index.html", context)


