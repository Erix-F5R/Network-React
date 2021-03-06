
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("user/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<int:post_id>", views.edit, name="edit"),

    ##API
    path("editor/<int:post_id>", views.editor, name="editor"),
    path("getlikes/<int:post_id>", views.getlikes, name="getlikes"),
    path("postlike/<int:post_id>",views.postlike, name="postlike"),
    path("all_posts", views.all_posts, name="all-posts"),
]
