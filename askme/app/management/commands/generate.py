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
    tags = [Tag(name=gen.word()[:20]) for _ in range(Count.TAGS)]
    Tag.objects.bulk_create(tags)

    # USER
    users = [User(username=f"username{i}", first_name=gen.first_name(), last_name=gen.last_name(),
                  password=gen.password()) for i in range(Count.USERS)]
    User.objects.bulk_create(users)
    users = User.objects.exclude(is_superuser=True)
    profiles = [Profile(user=user, avatar=choice(avatars)) for user in users]
    Profile.objects.bulk_create(profiles)

    profiles = Profile.objects.all()
    # likes = Like.objects.all()
    tags = Tag.objects.all()

    # LIKE
    likes = [Like(to_whom=choice(profiles), from_whom=choice(profiles)) for _ in range(Count.CONTENT_LIKES)]
    Like.objects.bulk_create(likes)

    # QUESTION
    questions = [Question(author=choice(profiles),
                          title=f"Question{i}",
                          text=gen.text(),
                          #like=likes[i],
                          ) for i in range(Count.QUESTIONS)]
    Question.objects.bulk_create(questions)
    questions = Question.objects.all()
    for i in range(Count.QUESTIONS):
        questions[i].tags.set([tags[i * randint(1, 10) % Count.TAGS] for _ in range(randint(1, 4))])

    questions = Question.objects.all()

    # ANSWER
    answers = [Answer(author=choice(profiles),
                      question=choice(questions),
                      text=gen.text(),
                      # like=likes[i],
                      correct=choice([True, False]),
                      ) for i in range(Count.QUESTIONS)]
    Answer.objects.bulk_create(answers)


