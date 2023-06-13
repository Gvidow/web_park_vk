from django.urls import path
from .views import *
from django.conf.urls.static import static
from askme import settings

urlpatterns = [
    path('', index, name="index"),
    path('question/<int:id>', question, name="question"),
    path('profile/edit/', setting, name="settings"),
    path('logout/', logout, name="logout"),
    path("login/", log_in, name="login"),
    path("signup/", signup, name="signup"),
    path("tag/<str:tag>", search_by_tag, name="tag"),
    path("ask/", ask, name="ask"),
    path("hot/", hot, name="hot"),
    path("best/<int:id>", best_users, name="best"),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
