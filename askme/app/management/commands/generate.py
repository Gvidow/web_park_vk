import random

from app.models import Like, Tag, User, Profile, Question, Answer
from django.utils import timezone
from datetime import timedelta
from random import randint, choice
from faker import Faker


class Count:
    USERS = 0
    QUESTIONS = 0
    ANSWERS = 0
    TAGS = 0
    CONTENT_LIKES = 0

    @classmethod
    def set_values(cls, ratio):
        cls.USERS = ratio
        cls.QUESTIONS = ratio * 10
        cls.ANSWERS = ratio * 100
        cls.TAGS = ratio
        cls.CONTENT_LIKES = ratio * 200


def fill(ratio):
    Count.set_values(ratio)
    gen = Faker()
    avatars = ["1.png", "2.jpeg", "3.png", "4.jpg", "5.jpg", "6.png", "7.png", "8.png"]
    avatars = [f"static/img/avatar/user{avatar}" for avatar in avatars]

    # TAG
    last_tag = Tag.objects.only("id").order_by("-id")
    try:
        last_id = last_tag[0].id
    except IndexError:
        last_id = 0
    tags = [Tag(id=i, name=gen.word()[:20] + str(i)) for i in range(last_id + 1, last_id + 1 + Count.TAGS)]
    Tag.objects.bulk_create(tags)

    # USER
    # get last user
    last_user = User.objects.only("id").order_by("-id")
    try:
        last_id = last_user[0].id
    except IndexError:
        last_id = 0
    users = [User(id=i, username=f"username{i}", first_name=gen.first_name(), last_name=gen.last_name(),
                  password=gen.password()) for i in range(last_id + 1, last_id + 1 + Count.USERS)]
    User.objects.bulk_create(users)

    users = User.objects.exclude(is_superuser=True).filter(id__gt=last_id)
    profiles = [Profile(user=user, avatar=choice(avatars)) for user in users]
    Profile.objects.bulk_create(profiles)

    profiles = Profile.objects.all()
    count_profiles = len(profiles)
    tags = Tag.objects.all()

    # QUESTION
    questions = [Question(author=choice(profiles),
                          title=f"Question{i}",
                          text=gen.text(),
                          ) for i in range(Count.QUESTIONS)]
    Question.objects.bulk_create(questions)
    questions = Question.objects.all()

    # ANSWER
    answers = [Answer(author=choice(profiles),
                      question=choice(questions),
                      text=gen.text(),
                      correct=choice([True, False]),
                      ) for _ in range(Count.QUESTIONS)]
    Answer.objects.bulk_create(answers)

    # LIKE FOR QUESTION
    count_question_with_likes = randint(0, Count.CONTENT_LIKES)
    likes = [Like(from_whom=profiles[i % count_profiles], question=random.choice(list(set(questions) - set(profiles[i % count_profiles].questions.all()))),
                  event=choice(("+", "+")))
             for i in range(count_question_with_likes)]
    Like.objects.bulk_create(likes)

    # LIKE FOR ANSWER
    likes = [Like(from_whom=profiles[i % count_profiles], answer=random.choice(list(set(answers) - set(profiles[i % count_profiles].answers.all()))),
                  event=choice(("+", "+")))
             for i in range(count_question_with_likes, Count.CONTENT_LIKES)]
    Like.objects.bulk_create(likes)

    for i in range(Count.QUESTIONS):
        questions[i].tags.set([tags[i * randint(1, 10) % Count.TAGS] for _ in range(randint(1, 4))])

