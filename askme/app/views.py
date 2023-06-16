from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import auth
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Question, Tag, Answer, Profile, Like
from django.urls import reverse
from .forms import LoginForm, RegisterForm, ProfileEditForm, QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from pkg.ajax import login_required_ajax, HttpResponseAjax, HttpResponseAjaxError
from django.db import transaction
from cent import Client
from django.forms import model_to_dict
from askme.settings import CENTRIFUGO_ADDR


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    questions = Question.objects.get_questions_all()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "tags": TAGS,
               "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
        context["likes_question"] = request.user.profile.likes_question()
        context["dislikes_question"] = request.user.profile.dislikes_question()
    return render(request, "index.html", context)


client = Client(CENTRIFUGO_ADDR + "/api", api_key="apikey", timeout=1)

@require_http_methods(["GET", "POST"])
def question(request, id: int):
    print("=====QUESTION=======")
    print(CENTRIFUGO_ADDR)
    chan_id = f"question_{id}"
    try:
        question = Question.objects.get_by_id(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    if request.method == "GET":
        answer_form = AnswerForm()
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login") + f"?continue={reverse('question', args=[id])}%23answer-form")
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(request.user, question)
            print(answer, type(answer), model_to_dict(answer))
            client.publish(f"question_{id}", model_to_dict(answer))
            answers_cou = question.answers.count()
            num_page = (answers_cou // 10) + 1
            return HttpResponseRedirect(reverse("question", args=[id]) + f"?page={num_page}#answer-{answer.id}")

    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    answers = question.answers.order_by("date")
    context = {
        "question": question,
        "page_obj": paginate(answers, request),
        "tags": TAGS, "best_members": MEMBERS,
        "form": answer_form,
    }
    if request.user.is_authenticated:
        context["user_data"] = request.user
        context["likes_question"] = [id] if request.user.profile.is_liked_question(id) else None
        context["dislikes_question"] = [id] if context["likes_question"] is None and \
                                            request.user.profile.is_disliked_question(id) else None
        context["likes_answer"] = request.user.profile.likes_answer()
        context["dislikes_answer"] = request.user.profile.dislikes_answer()
    return render(request, "question.html", context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(["GET", "POST"])
def setting(request):
    if request.method == "GET":
        setting_form = ProfileEditForm(initial=dict(upload_avatar=request.user.profile.avatar,
                                                    username=request.user.username, first_name=request.user.first_name,
                                                    last_name=request.user.last_name, email=request.user.email))
    else:
        setting_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if setting_form.is_valid():
            setting_form.save()
            return HttpResponseRedirect(reverse("settings"))

    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS, "best_members": MEMBERS,
        "form": setting_form,
    }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "settings.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def log_in(request):
    continue_url = request.GET.get("continue")
    if continue_url is None or continue_url[0] != "/":
        continue_url = "/"

    if request.method == "GET":
        login_form = LoginForm()
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(continue_url)
            else:
                login_form.add_error(None, "Incorrect login or password")

    setattr(login_form, "continue_url", continue_url)
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS,
        "best_members": MEMBERS,
        "form": login_form,
    }
    return render(request, "login.html", context)


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "GET":
        register_form = RegisterForm()
    else:
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            user = auth.authenticate(request, **register_form.cleaned_data)
            if user:
                auth.login(request, user)
            return HttpResponseRedirect("/")
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"tags": TAGS, "best_members": MEMBERS,
               "form": register_form}
    return render(request, "register.html", context)


def search_by_tag(request, tag: str):
    try:
        questions = Question.objects.by_tag(tag)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "tag": tag,
               "tags": TAGS, "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
        context["likes_question"] = request.user.profile.likes_question()
        context["dislikes_question"] = request.user.profile.dislikes_question()
    return render(request, "tag.html", context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(["GET", "POST"])
def ask(request):
    if request.method == "GET":
        question_form = QuestionForm()
    else:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_id = question_form.save(request.user)
            return HttpResponseRedirect(reverse("question", args=[question_id]))

    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {
        "tags": TAGS,
        "best_members": MEMBERS,
        "form": question_form,
    }
    if request.user.is_authenticated:
        context["user_data"] = request.user
    return render(request, "ask.html", context)


def hot(request):
    questions = Question.objects.hot_questions()
    TAGS = Tag.objects.all()[:20]
    MEMBERS = Profile.objects.best()
    context = {"page_obj": paginate(questions, request),
               "tags": TAGS, "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
        context["likes_question"] = request.user.profile.likes_question()
        context["dislikes_question"] = request.user.profile.dislikes_question()
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
               "tags": TAGS, "best_members": MEMBERS,
               }
    if request.user.is_authenticated:
        context["user_data"] = request.user
        context["likes_question"] = request.user.profile.likes_question()
        context["dislikes_question"] = request.user.profile.dislikes_question()
    return render(request, "index.html", context)


@login_required_ajax
@require_POST
@transaction.atomic
def vote_up_question(request):
    question_id = request.POST.get("question_id")
    vote = request.POST.get("vote")

    if question_id is None:
        return HttpResponseAjaxError(code="notfound_id", message="question id required")
    if vote is None:
        return HttpResponseAjaxError(code="notfound_vote", message="vote required")

    try:
        question = Question.objects.get(id=question_id)
        valuation = request.user.profile.likes.update_vote(request.user.profile, question, vote)
        return HttpResponseAjax(count_likes=question.count_like(), count_dislikes=question.count_dislike(),
                                valuation=valuation)
    except ObjectDoesNotExist:
        return HttpResponseAjaxError(code="notfound_question", message="the issue with this id was not found")
    except Exception as e:
        return HttpResponseAjaxError(code="db_error", message=str(e))


@login_required_ajax
@require_POST
def vote_up_answer(request):
    answer_id = request.POST.get("answer_id")
    vote = request.POST.get("vote")

    if answer_id is None:
        return HttpResponseAjaxError(code="notfound_id", message="answer id required")
    if vote is None:
        return HttpResponseAjaxError(code="notfound_vote", message="vote required")

    try:
        answer = Answer.objects.get(id=answer_id)
        valuation = request.user.profile.likes.update_vote(request.user.profile, answer, vote)
        return HttpResponseAjax(count_likes=answer.count_like(), count_dislikes=answer.count_dislike(),
                                valuation=valuation)
    except ObjectDoesNotExist:
        return HttpResponseAjaxError(code="notfound_answer", message="the issue with this id was not found")
    except Exception as e:
        return HttpResponseAjaxError(code="db_error", message=str(e))


@login_required_ajax
@require_POST
@transaction.atomic
def correct(request):
    answer_id = request.POST.get("answer_id")

    if answer_id is None:
        return HttpResponseAjaxError(code="notfound_id", message="answer id required")

    try:
        answer = Answer.objects.get(id=answer_id)
        if request.user.profile != answer.author:
            return HttpResponseAjaxError(code="no_rights",
                                         message="only the author of the question can mark the correct questions")
        answer.update_correct()
        return HttpResponseAjax(correct=answer.correct)
    except ObjectDoesNotExist:
        return HttpResponseAjaxError(code="notfound_answer", message="the issue with this id was not found")
    except Exception as e:
        return HttpResponseAjaxError(code="db_error", message=str(e))
