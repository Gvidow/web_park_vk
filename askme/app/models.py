from django.db import models
from django.db.models import Manager, Count
from django.contrib.auth.models import User
from random import choice
from django.utils import timezone
from datetime import timedelta



class ProfileManager(Manager):
    def best(self):
        users = Profile.objects.all()
        stat = [(user, self.count_like(user)) for user in users]
        return [user[0] for user in sorted(stat, key=lambda x: x[1], reverse=True)[:10]]


    def count_like(self, profile):
        return len(Like.objects.filter(to_whom=profile))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to="static/img/avatar", default="static/img/default-avatar.jpg")

    def __str__(self):
        return f"{self.user.username[-1]} {self.user.first_name} {self.user.last_name} {self.id=}"

    objects = ProfileManager()


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class Like(models.Model):
    to_whom = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="to_whom")
    from_whom = models.ForeignKey("Profile", on_delete=models.PROTECT, related_name="from_whom")
    date = models.DateTimeField(auto_now=True)



class QuestionManager(Manager):
    def count_answer(self, question):
        return len(Answer.objects.answers_to_question(question))

    def by_tag(self, tag):
        questions = Question.objects.all()
        return filter(lambda q: tag in map(lambda t: t.name, q.tags.all()), questions)

    def hot_questions(self):
        return Question.objects.filter(date__gte=timezone.now() - timedelta(days=7))


class Question(models.Model):
    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    # like = models.OneToOneField("Like", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")

    objects = QuestionManager()

    def __str__(self):
        return f"{self.title} from {self.author.user.username} {self.id=}"


class AnswerManage(Manager):
    def answers_to_question(self, question):
        return Answer.objects.filter(question=question)


class Answer(models.Model):
    author = models.ForeignKey("Profile", on_delete=models.PROTECT)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    # like = models.OneToOneField("Like", on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    objects = AnswerManage()


class AUTHORIZED:
    status = True
    user = None

def get_user():
    return AUTHORIZED.user
    try:
        return Profile.objects.get(id=ok)
    except models.ObjectDoesNotExist:
        return None

def log_out():
    AUTHORIZED.status = False
    AUTHORIZED.user = None
#
#
def log_in():
    AUTHORIZED.status = True
    AUTHORIZED.user = choice(Profile.objects.all())
