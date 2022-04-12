from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Follower, User, Post
from.forms import NewPostForm


def index(request):

    if request.method == 'POST':

        form = NewPostForm(request.POST)

        if form.is_valid():

            body = form.cleaned_data["body"]
            post = Post(body=body,
                        user = User.objects.get(pk=request.user.id))
            post.save()    

    return render(request, "network/index.html", {"form": NewPostForm()})

def profile(request, username):
    
    viewed_user = User.objects.get(username=username)
    logged_in_user = request.user 
    posts = Post.objects.filter(user=viewed_user).order_by("-date")

    if request.method == "POST":        
        if request.POST.get("submit") == "Follow":
            if viewed_user != logged_in_user:
                follower = Follower(following=logged_in_user, followed=viewed_user )
                follower.save()
            return HttpResponseRedirect(f"/user/{viewed_user}")

       

    
    following_count = Follower.objects.filter(following=viewed_user).count
    followed_count = Follower.objects.filter(followed=viewed_user).count
    
    
    return render(request,"network/profile.html", {"user": viewed_user,"posts": posts, "following_count": following_count, "followed_count":followed_count})

def all_posts(request):

    all_posts = Post.objects.all().order_by("-date")

    return render(request, "network/all_posts.html", {"all_posts": all_posts} )

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
