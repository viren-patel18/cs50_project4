
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("update/<int:post_id>", views.update, name="update"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like")
]
