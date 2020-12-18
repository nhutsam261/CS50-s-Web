from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
import json

from .models import User, Post, Profile, Like
from .my_forms import UserRegisterForm


def index(request):
    all_posts = Post.objects.order_by('-createdDate')
    paginator = Paginator(all_posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })


def register(request):
    if request.method == 'POST':
        f = UserRegisterForm(request.POST)
        if f.is_valid():
            f.save()
            # username = f.cleaned_data['username']
            messages.success(request, f'Your account has been created! You can now login!')
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Failed to create new account. Please check again the information")
            return render(request, "network/register.html", {
                "form": f
            })


    return render(request, "network/register.html", {
        "form": UserRegisterForm()
    })

@login_required
@csrf_exempt
def new_post(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    data_content = data.get('content')
    if data_content == "":
        return JsonResponse({"error": "The post content must not be empty"}, status=400)
    
    post = Post.objects.create(creator=request.user.profile, content=data_content)
    post.save()
    return JsonResponse({"message": "Your post created successfully."}, status=201)


@csrf_exempt
@login_required
def post(request, post_id):
    try:
        post = Post.objects.get(creator=request.user.profile, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(post.serialize())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        post.content = data['content']
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    liked_state = False
    if Like.objects.filter(byProfile=request.user.profile, onPost=post):
        like = Like.objects.get(byProfile=request.user.profile, onPost=post)
        like.delete()
    else:
        like = Like.objects.create(byProfile=request.user.profile, onPost=post)
        like.save()
        liked_state = True

    num_likes = post.likes.count()
    return JsonResponse({
        "likes": num_likes,
        "liked_state": liked_state
        })

@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    posts = Post.objects.filter(creator=p).order_by('-createdDate')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    following_state = True if p in request.user.profile.following.all() else False
    followers_num = p.followers.count()
    following_num = p.following.all().count()

    return render(request, "network/profile.html", {
        'u': u,
        'page_obj': page_obj,
        'following_state': following_state,
        'followings': following_num,
        'followers': followers_num
    })


@login_required 
def follow_unfollow(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if profile not in request.user.profile.following.all():
        request.user.profile.following.add(profile)
        return JsonResponse({'following_state': True})
    else:
        request.user.profile.following.remove(profile)
        return JsonResponse({'following_state': False})


@login_required
def following_posts(request):
    followings = request.user.profile.following.all()
    posts = Post.objects.filter(creator__in=followings).order_by('-createdDate')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'page_obj': page_obj
    })







