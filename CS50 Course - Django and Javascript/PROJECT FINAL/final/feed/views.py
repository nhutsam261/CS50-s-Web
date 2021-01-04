import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Post, Like, Comment
from .my_forms import CreatePostForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def index(request):
    posts = Post.objects.order_by('-date_posted')
    liked_post = [p for p in Post.objects.all() if Like.objects.filter(byProfile=request.user, onPost=p)]
    return render(request, 'feed/index.html', {
        'posts': posts,
        'liked_post': liked_post
    })


@csrf_exempt
@login_required
def post(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    is_liked = Like.objects.filter(onPost=post, byProfile=request.user)

    if request.method == 'POST':
        data = json.loads(request.body)
        print("JSON: ", data)
        if data.get('content') != "":
            cmt, created = Comment.objects.get_or_create(onPost=post, content=data.get('content'), createdBy=request.user)
            return JsonResponse(cmt.serialize())
        else:
            return JsonResponse({'message': 'failed'})
    
    return render(request, "feed/post.html", {
        'post': post,
        'is_liked': is_liked,
    })

@login_required
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    liked = False
    like = Like.objects.filter(onPost=post, byProfile=request.user)

    if like:
        like.delete()
    else:
        liked = True
        Like.objects.create(onPost=post, byProfile=request.user)
    return JsonResponse({'liked': liked}, status=201)


@login_required
def create_post(request):
    if request.method == 'POST':
        f = CreatePostForm(request.POST, request.FILES)
        if f.is_valid():
            post = f.save(commit=False)
            post.creator = request.user
            post.save()
            
        return HttpResponseRedirect(reverse('home'))