from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DeleteView
from .models import User, Profile, Post, Comments, Likes, UserFollowing
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
import json

# List all Post 
class PostListView(ListView):
    model = Post
    template_name = 'network/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked_posts = self.request.user.likes.all()
            liked_posts = [liked_post.post for liked_post in liked_posts]
            user_posts = self.request.user.posts.all()
            context['liked_posts'] = liked_posts
            context['user_posts'] = user_posts
        return context
    def get_queryset(self):
        return Post.objects.all().order_by('-date_posted')

class FollowingListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'network/following.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FollowingListView, self).get_context_data(**kwargs)
        liked_posts = self.request.user.likes.all()
        liked_posts = [liked_post.post for liked_post in liked_posts]
        context['liked_posts'] = liked_posts
        return context

    def get_queryset(self):
        following_users = self.request.user.following.all()
        id_users =[following.following_user.id for following in following_users]
        print('id: ' , id_users)
        return Post.objects.filter(user__in=id_users).order_by('-date_posted')

class UserPostListView(LoginRequiredMixin, ListView):

    model = Post
    template_name = 'network/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        liked_posts = self.request.user.likes.all()
        context['liked_posts'] = liked_posts
        return context

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-date_posted')

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


@login_required
def posts(request):
    

    all_posts = Post.objects.all()
    all_posts.order_by('-date_posted').all()
    results = [post.serialize() for post in all_posts]
    numOfPage = 10
    p = Paginator(results, numOfPage)
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)

    liked_posts = request.user.likes.all()
    userPosts = request.user.post.all()
    results = []
    for post in all_posts:
        p = post.serialize()
        if post in liked_posts:
            p['liked'] = 1
        results.append(p)
    print(results)

    return JsonResponse(results, safe=False)


@login_required
def search_post(request, post_id):
    try:
        post = Post.objects.filter(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'post':'post not found'}, status=404)
    if request.method == 'POST':
        return JsonResponse(post.serialize())

    



@csrf_exempt
@login_required
def post(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'PUT method is required'}, status = 400)
    jsonContent = json.loads(request.body)
    description  = jsonContent.get('description', '')
    if description == '':
        return JsonResponse({'error': 'Content must not empty !!'}, status=400)
    post = Post(user=request.user, description=description)
    post.save()
    return JsonResponse({'message': 'Post successfully'}, status=201)





@login_required
@csrf_exempt
def like(request, post_id):

    
    if request.method == 'PUT':
        user = request.user
        post = Post.objects.filter(pk=post_id)[0]
        print('post_id2: ', post_id)
        data = json.loads(request.body)
        checkLiked = data.get('liked')
        print('checkLiked: ', checkLiked)
        print('type Liked: ', type(checkLiked))
        if checkLiked == False:
            print('false')
            Likes.objects.create(user=user, post=post)
        else:
            liked = Likes.objects.filter(user=user, post=post)
            liked.delete()    
        return JsonResponse({'success': 'OK'}, status=204)
    return JsonResponse({'error': 'GET or PUT method is required'})

# follow user in database
@login_required
def follow(request, following_user_id):
    user = request.user
    following_user = User.objects.filter(pk=following_user_id).first()
    print('following_user: ', following_user.username)
    followed = UserFollowing.objects.filter(user=user, following_user = following_user).first()

    if followed:
        followed.delete()
    else:
        UserFollowing.objects.create(user=user, following_user=following_user)
    
    return HttpResponseRedirect(reverse("profile", kwargs={'slug':user.profile.slug}))

@login_required
@csrf_exempt
def edit(request, post_id):
   
    if request.method != 'PUT':
        return JsonResponse({'error': 'PUT method is required'}, status = 400)
    post = Post.objects.filter(pk=post_id)[0]
    jsonContent = json.loads(request.body)
    description  = jsonContent.get('description', '')
    print('description: ', description)
    if description == '':
        return JsonResponse({'error': 'Content must not empty !!'}, status=400)
    post.description = description
    post.save()
    return JsonResponse({'message': 'Post successfully'}, status=201)

@login_required
@csrf_exempt
def comments(request, post_id):

    try:
        post = Post.objects.filter(pk=post_id)[0]
    except Post.DoesNotExist:
        return JsonResponse({"error": "Comment not found."}, status=404)

    if request.method == 'GET':
        cmts = post.comments.all().order_by('-date_commented')
        results = [cmt.serialize() for cmt in cmts]
        return JsonResponse(results, safe=False)

    elif request.method == 'PUT':
        jsonCotent = json.loads(request.body)
        content = jsonCotent.get('content', '')
        print('content: ', content)
        if content == '':
            return JsonResponse({'error': 'Comment must not empty !!!'})
        cmt = Comments(user=request.user, post=post, content=content)
        cmt.save()
        return JsonResponse({'message': 'Post successfully'}, status=201)

def profile(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    profileUser = Profile.objects.filter(slug=slug).first()
    user = profileUser.user
    posts = user.posts.all()
    followers = user.followers.all()
    following = user.following.all()
    currentUserFollowing = request.user.following.all()
    currentUserFollowing = [following.following_user for following in currentUserFollowing]
    user_posts = request.user.posts.all()
    liked_posts = request.user.likes.all()
    liked_posts = [liked_post.post for liked_post in liked_posts]
    print(liked_posts)
    context = {
        'user': user,
        'followers': followers,
        'following': following,
        'posts': posts,
        'current_following': currentUserFollowing,
        'user_posts':user_posts,
        'liked_posts': liked_posts,
    }

    return render(request, 'network/profile.html', context)
    

    