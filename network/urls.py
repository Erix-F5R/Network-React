
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("user/<str:username>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<int:post_id>", views.edit, name="edit"),

    ##API
    path("editor/<int:post_id>", views.editor, name="editor"),
    ##path("likes/<int:post_id>",views.like, name="like"),
    path("getlikes/<int:post_id>", views.getlikes, name="getlikes"),
    path("all_posts", views.all_posts, name="all-posts"),
]
