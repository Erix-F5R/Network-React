from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt

import json

from .models import Follower, User, Post, Like
from .forms import NewPostForm


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


    return render(request, "network/edit.html", {"form":post_form,"current_user": request.user,"post":post_id})

##API
@csrf_exempt
def editor(request,post_id):  
    
    try:
        post = Post.objects.get(id = post_id)
        user = request.user
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if not post.user == user:
        return JsonResponse({"error": "You may only edit your own posts."}, status=404)

    text = json.loads(request.body).get("text")
    post.body = text
    post.save()


    return HttpResponse(status=204)



##GET Request
def getlikes(request, post_id):

    try:
        post = Post.objects.get(id = post_id)
        user = request.user
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "GET":
        count = Like.objects.filter(post = post).count()
        
        if user.is_anonymous:
            like_exists = False
        else:
            like_exists = Like.objects.filter(user=user,post=post).exists()

        if like_exists:
            return JsonResponse({"count": count, 'like': 'false'})
        else:
            return JsonResponse({"count": count, 'like': 'true'})

    return HttpResponse(status=204)
##POST Request

def postlike(request, post_id):

    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    like = data.get("like")

    if like:
        try:
            post = Post.objects.get(id = post_id)
            user = request.user
        except:
            return JsonResponse({"error": "Post not found."}, status=404)

        ##Like
        if not Like.objects.filter(user=user,post=post).exists():
            newLike = Like(user=user, post=post)
            newLike.save()
            return JsonResponse({'like': 'true'})
        ##Unlike
        else:
            Like.objects.filter(user=user,post=post).delete()
            return JsonResponse({'like': 'false'})

    
    return HttpResponse(status=204)

def profile(request, username):
    
    viewed_user = User.objects.get(username=username)
    logged_in_user = request.user 
    ifFollows = Follower.objects.filter(following=logged_in_user, followed=viewed_user ).exists()

    #Pagination
    p = Paginator(Post.objects.filter(user=viewed_user).order_by("-date"),10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    #posts = Post.objects.filter(user=viewed_user).order_by("-date")

    if request.method == "POST":        
        if request.POST.get("submit") == "Follow":
            if viewed_user != logged_in_user:
                #Check if already follows                
                if not ifFollows:
                    follower = Follower(following=logged_in_user, followed=viewed_user ) 
                    follower.save()
                            
        elif request.POST.get("submit") == "Unfollow":
            if viewed_user != logged_in_user:
                Follower.objects.filter(following=logged_in_user, followed=viewed_user ).delete()
                
        return HttpResponseRedirect(f"/user/{viewed_user}")

    
    following_count = Follower.objects.filter(following=viewed_user).count
    followed_count = Follower.objects.filter(followed=viewed_user).count
    
    
    return render(request,"network/profile.html", {"current_user": logged_in_user,
                                                    "viewed_user": viewed_user,
                                                    "posts": posts,
                                                    "following_count": following_count,
                                                    "followed_count":followed_count,
                                                    "ifFollows":ifFollows})

def all_posts(request):
    
    all_posts = Post.objects.all().order_by("-date")

    return render(request, "network/all_posts.html", {"all_posts": all_posts, "current_user": request.user} )

def following(request):
    current_user = request.user
    following =  Follower.objects.filter(following=current_user)
    following_posts = Post.objects.none()

    for u in following:

        following_posts = following_posts.union( Post.objects.filter(user = u.followed) )

    print(following_posts, following)

    return render(request, "network/following.html",{ "following_posts": following_posts.order_by("-date"), "current_user": request.user} )

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
