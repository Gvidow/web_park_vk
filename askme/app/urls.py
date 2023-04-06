from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('question/<int:id>', question, name="question"),
    path('setting/<str:id>', setting, name="settings"),
    path('logout/', logout, name="logout"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("tag/<str:tag>", search_by_tag, name="tag"),
    path("ask/", ask, name="ask"),
]
