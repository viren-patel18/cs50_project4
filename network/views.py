import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.core.paginator import Paginator

from .models import *

@csrf_exempt
def index(request):
    if request.method == "POST":
        data = request.POST
        content = data.get("content", "default")
        post = Post(
            content = content,
            author = request.user
        )
        post.save()
        # post = Post.objects.create(
        #     content = request.POST["content"],
        #     author = request.user
        # )
        # return JsonR  esponse({"message": "Posted successfully."}, status=201)
    
    posts = Post.objects.all().order_by("-id")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(1 if page_number is None else page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "page_range": range(1, page_obj.paginator.num_pages)
    })

class PostList(ListView):
    paginate_by = 2
    model = Post

@csrf_exempt
def update(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": f"{content}"}, status = 400)

    data = json.loads(request.body)
    content = data.get("content", "default")
    post = Post.objects.get(id = post_id)
    post.content = content
    post.save()
    return JsonResponse({"message": f"Message edited successfully. {content}"}, status = 201)

@csrf_exempt
def like(request, post_id):

    if request.method != "PUT":
        return JsonResponse({"error": "error processing request."}, status = 400)

    post = Post.objects.get(id = post_id)
    liked = 0

    if request.user in post.likedBy.all():
        post.likedBy.remove(request.user)
    else:
        post.likedBy.add(request.user)
        liked = 1

    post.save()
    return JsonResponse({"liked": f"{liked}", "postLikes": len(post.likedBy.all())}, status = 201)


@csrf_exempt
def profile(request, user_id):
    user = User.objects.get(id = user_id)
    following = 0
    if request.method == "PUT":
        if request.user in user.followers.all():
            user.followers.remove(request.user)
            request.user.following.remove(user)
        else:
            user.followers.add(request.user)
            request.user.following.add(user)
            following = 1
        user.save()
        request.user.save()
        return JsonResponse({"following": f"{following}", "followerCount": len(user.followers.all())}, status = 201)
    
    posts = user.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile_user": user,
        "page_obj": page_obj,
        "page_range": range(1, page_obj.paginator.num_pages)
    })

def following(request):
    posts = Post.objects.filter(author__in=request.user.following.all())
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

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
