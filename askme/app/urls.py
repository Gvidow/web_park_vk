from django.urls import path
from .views import index, question

urlpatterns = [
    path('', index, name="index"),
    path('question/<int:id>', question, name="question")
]
