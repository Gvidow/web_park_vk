from django.db import models
from random import choice


class User:
    def __init__(self, id, avatar):
        self.id = id
        self.avatar = avatar
        self.name = "Dr. Pepper"


class Question:
    def __init__(self, id, author, title, text):
        self.id = id
        self.author = author
        self.title = title
        self.text = text


def get_questions():
    return [{
        "id": q.id,
        "title": q.title,
        "text": q.text,
        "avatar": "img/" + q.author.avatar,
    } for q in QUESTIONS
    ]


def get_user(ok):
    if not ok:
        return None
    else:
        return USERS[0]


COUNT_USERS = 6
COUNT_QUESTION = 10

PICTURES = ["user1.png", "user2.jpeg", "user3.png"]

USERS = [User(i, choice(PICTURES)) for i in range(COUNT_USERS)]

QUESTIONS = [Question(i, choice(USERS), f"Title {i}", f"Text {i}") for i in range(COUNT_QUESTION)]

