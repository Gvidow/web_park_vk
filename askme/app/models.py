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

class Answer:
    def __init__(self, id, author, question, text, corect, count_like):
        self.id = id
        self.author = author
        self.question = question
        self.text = text
        self.corect = corect
        self.count_like = count_like


def get_questions():
    return [{
        "id": q.id,
        "title": q.title,
        "text": q.text,
        "avatar": q.author.avatar,
    } for q in QUESTIONS
    ]

def get_question(id):
    for q in QUESTIONS:
        if q.id == id:
            return q


def get_user(ok):
    if not ok:
        return None
    else:
        return USERS[0]
    
def get_responses(question_id):
    res = []
    for a in ANSWERS:
        if a.question.id == question_id:
            res.append(a)
    return res



COUNT_USERS = 6
COUNT_QUESTION = 10
COUNT_ANSWER = 30

PICTURES = ["img/user1.png", "img/user2.jpeg", "img/user3.png"]

USERS = [User(i, choice(PICTURES)) for i in range(COUNT_USERS)]

QUESTIONS = [Question(i, choice(USERS), f"Title {i}", f"Text {i}") for i in range(COUNT_QUESTION)]

ANSWERS = [Answer(i, choice(USERS), choice(QUESTIONS), f"{i} I think everything will be fine", choice([True, False]), 12 * i) for i in range(COUNT_ANSWER)]

