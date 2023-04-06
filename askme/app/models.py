from django.db import models
from random import choice, randint
from faker import Faker


class User:
    def __init__(self, id, avatar, name):
        self.id = id
        self.avatar = avatar
        self.name = name


class Question:
    def __init__(self, id, author, title, text, count_like, count_answer, tags):
        self.id = id
        self.author = author
        self.title = title
        self.text = text
        self.count_like = count_like
        self.count_answer = count_answer
        self.tags = tags


class Answer:
    def __init__(self, id, author, question, text, correct, count_like):
        self.id = id
        self.author = author
        self.question = question
        self.text = text
        self.correct = correct
        self.count_like = count_like


def get_questions():
    return QUESTIONS


def get_question(id):
    for q in QUESTIONS:
        if q.id == id:
            return q


def get_user(ok):
    if ok is False:
        return None
    elif ok is True:
        return USERS[randint(0, COUNT_USERS - 1)]
    ok = int(ok)
    if ok < 0 or ok >= len(USERS):
        return None
    return USERS[int(ok)]

    
def get_answers(question_id):
    res = []
    for a in ANSWERS:
        if a.question.id == question_id:
            res.append(a)
    return res


class AUTHORIZED:
    status = True


def log_out():
    AUTHORIZED.status = False


def log_in():
    AUTHORIZED.status = True


def question_by_tag(tag):
    res = []
    for question in QUESTIONS:
        if tag in question.tags:
            res.append(question)
    return res


gen = Faker()

COUNT_USERS = 6
COUNT_QUESTION = 50
COUNT_ANSWER = 30

PICTURES = ["img/user3.png", "img/user2.jpeg", "img/user3.png", "img/user4.jpg", "img/user5.jpg",
            "img/user6.png", "img/user7.png", "img/user8.png"]

TAGS = [gen.word() for _ in range(8)]
MEMBERS = [gen.name() for _ in range(8)]

USERS = [User(i, choice(PICTURES), gen.name()) for i in range(COUNT_USERS)]

QUESTIONS = [Question(i, choice(USERS), f"question {i}", gen.text(), randint(0, 1000), 0, [choice(TAGS) for _ in range(randint(1, 5))]) for i in range(COUNT_QUESTION)]

ANSWERS = [Answer(i, choice(USERS), choice(QUESTIONS), gen.text(),
                  choice([True, False]), randint(0, 1000)) for i in range(COUNT_ANSWER)]

for i in range(COUNT_QUESTION):
    QUESTIONS[i].count_answer = len(get_answers(QUESTIONS[i].id))
