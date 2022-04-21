from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt

import json

from .models import Follower, User, Post, Like
from.forms import NewPostForm


def index(request):

    if request.method == 'POST':

        form = NewPostForm(request.POST)

        if form.is_valid():

            body = form.cleaned_data["body"]
            post = Post(body=body,
                        user = User.objects.get(pk=request.user.id))
            post.save()    

    return render(request, "network/index.html", {"form": NewPostForm(),"current_user": request.user})

def edit(request, post_id):
    
    post = Post.objects.get(id=post_id)
    post_form = NewPostForm(instance=post, initial={'body':post.body})

    #IF POST
    #form = MyModelForm(request.POST, instance=my_record)

    return render(request, "network/edit.html", {"form":post_form,"current_user": request.user,"post":post_id})

##API
@csrf_exempt
def editor(request,post_id):  
    
    try:
        post = Post.objects.get(id = post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    text = json.loads(request.body).get("text")
    post.body = text
    post.save()


    return HttpResponse(status=204)


def profile(request, username):


    
    viewed_user = User.objects.get(username=username)
    logged_in_user = request.user 

    #Pagination
    p = Paginator(Post.objects.filter(user=viewed_user).order_by("-date"),10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    #posts = Post.objects.filter(user=viewed_user).order_by("-date")

    if request.method == "POST":        
        if request.POST.get("submit") == "Follow":
            if viewed_user != logged_in_user:
                follower = Follower(following=logged_in_user, followed=viewed_user )
                follower.save()
            return HttpResponseRedirect(f"/user/{viewed_user}")

       

    
    following_count = Follower.objects.filter(following=viewed_user).count
    followed_count = Follower.objects.filter(followed=viewed_user).count
    
    
    return render(request,"network/profile.html", {"current_user": logged_in_user,"user": viewed_user,"posts": posts, "following_count": following_count, "followed_count":followed_count})

def all_posts(request):

    all_posts = Post.objects.all().order_by("-date")

    return render(request, "network/all_posts.html", {"all_posts": all_posts, "current_user": request.user} )

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
