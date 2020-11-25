from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import NewCommentForm, NewPostForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comments, Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from notifications.signals import notify
from django import forms
from django.utils import timezone

class PostListView(ListView):
    model = Post
    template_name = 'feed/home.html'
    context_object_name = 'posts'    
    ordering = ['-date_posted']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            unread_nofi = self.request.user.notifications.unread()
            print(self.request.user.notifications.__dict__)
            read_nofi = self.request.user.notifications.read()
            print("new notification: ", len(unread_nofi))
            for nofi in unread_nofi:
                print(nofi)
            
            userPost = Post.objects.filter(user=self.request.user)
            liked = [i for i in Post.objects.all() if Like.objects.filter(user = self.request.user, post=i)]
            context['liked_post'] = liked
            context['userPost'] = userPost
            context['notifications'] = unread_nofi
            context['countNofi'] = len(unread_nofi)
            if len(read_nofi) > 5:
                read_nofi = read_nofi[:5]
            context['read'] = read_nofi
        return context
    
    def get_queryset(self):
        user = self.request.user
        print('len query: ', len(Post.objects.filter(likes__user__in=[user.id])))
        return Post.objects.filter(status=1).order_by('-date_posted')

class WinPostListView(ListView):
    model = Post
    template_name = 'feed/win.html'
    context_object_name = 'posts'    
    ordering = ['-date_closed']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(WinPostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            unread_nofi = self.request.user.notifications.unread()
            read_nofi = self.request.user.notifications.read()
            print("new notification: ", len(unread_nofi))
            for nofi in unread_nofi:
                print(nofi)
            
            userPost = Post.objects.filter(user=self.request.user)
            liked = [i for i in Post.objects.all() if Like.objects.filter(user = self.request.user, post=i)]
            context['liked_post'] = liked
            context['userPost'] = userPost
            context['notifications'] = unread_nofi
            context['countNofi'] = len(unread_nofi)
            if len(read_nofi) > 5:
                read_nofi = read_nofi[:5]
            context['read'] = read_nofi
        return context

    def get_queryset(self):
        user = self.request.user
        print('len qeury: ', len(Post.objects.filter(userBid = user, status = 0)))
        return Post.objects.filter(userBid = user, status = 0).order_by('-date_closed')
class ClosedPostListView(ListView):
    model = Post
    template_name = 'feed/closed.html'
    context_object_name = 'posts'    
    ordering = ['-date_closed']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ClosedPostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            unread_nofi = self.request.user.notifications.unread()
            read_nofi = self.request.user.notifications.read()
            print("new notification: ", len(unread_nofi))
            for nofi in unread_nofi:
                print(nofi)
            
            userPost = Post.objects.filter(user=self.request.user)
            liked = [i for i in Post.objects.all() if Like.objects.filter(user = self.request.user, post=i)]
            context['liked_post'] = liked
            context['userPost'] = userPost
            context['notifications'] = unread_nofi
            context['countNofi'] = len(unread_nofi)
            if len(read_nofi) > 5:
                read_nofi = read_nofi[:5]
            context['read'] = read_nofi
        return context

    def get_queryset(self):
        user = self.request.user
        print('len qeury: ', len(Post.objects.filter(likes__user__in=[user.id])))
        return Post.objects.filter(status=0).order_by('-date_closed')

class WatchListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'feed/watchlist.html'
    context_object_name = 'posts'    
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(WatchListView, self).get_context_data(**kwargs)

        user = self.request.user
        if self.request.user.is_authenticated:
            watchlist = [i for i in Post.objects.all() if Like.objects.filter(user = user, post=i)]
            print("len watchlist:", len(watchlist))
            context['watchlist'] = watchlist
            unread_nofi = self.request.user.notifications.unread()
            read_nofi = self.request.user.notifications.read()
            context['notifications'] = unread_nofi
            context['countNofi'] = len(unread_nofi)
            if len(read_nofi) > 5:
                read_nofi = read_nofi[:5]
            context['read'] = read_nofi
        return context

    def get_queryset(self):
        user = self.request.user
        print('len qeury: ', len(Post.objects.filter(likes__user__in=[user.id])))
        return Post.objects.filter(likes__user__in=[user.id], status = 1).order_by('-status')
        
class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'feed/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        liked = [i for i in Post.objects.filter(user=user) if Like.objects.filter(user = self.request.user, post=i)]
        context['liked_post'] = liked
        unread_nofi = self.request.user.notifications.unread()
        read_nofi = self.request.user.notifications.read()
        context['notifications'] = unread_nofi
        context['countNofi'] = len(unread_nofi)
        if len(read_nofi) > 5:
            read_nofi = read_nofi[:5]
        context['read'] = read_nofi
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(user=user).order_by('-date_posted')

@login_required
def seen(request):
    print('notification current user:', len(request.user.notifications.unread()))
    if request.method == 'POST':
        request.user.notifications.mark_all_as_read()
        return redirect('home')
    return redirect('home') 

@login_required
def close_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    post.status = 0
    post.data_closed = timezone.now
    post.save()
    nameOfListing = post.nameOfListing
    print('name of listing: ', nameOfListing)
    notify.send(user, recipient=user, verb=' - You closed post: ' + nameOfListing)
    if post.userBid:
        notify.send(post.userBid, recipient=post.userBid, verb=' - You are winner: ' + nameOfListing)
    return redirect(f'/post/{post.id}/')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_liked =  Like.objects.filter(user=user, post=post)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.user = user
            
            data.save()
            return redirect('post-detail', pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'feed/post_detail.html', {'post':post, 'is_liked':is_liked, 'form':form})

@login_required
def bid(request):
    user = request.user
    price = request.POST['price']
    pk = request.POST['pk']
    currentPost = Post.objects.filter(pk=pk)[0]
    print(currentPost)
    
    currentPost.bid = price
    
    if user == currentPost.user:
        currentPost.save()
        notify.send(user, recipient=user, verb=f'- Successful update post: {currentPost.nameOfListing}', )
        return redirect('home')
    userBid = currentPost.userBid 
    if userBid is not None:
        notify.send(user, recipient=userBid, verb=f'- {user.username} has bid more than you with bid  {price}')

    currentPost.userBid = user
    currentPost.save()
    if Like.objects.filter(user=user, post=currentPost).count() == 0:
        like = Like(user=user, post = currentPost)
        like.save()
    notify.send(user, recipient=user, verb=f'- Successful Bid Post: {currentPost.nameOfListing}', description=str(currentPost.id))
    
    return redirect('home')
        

@login_required
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            notify.send(user, recipient=user, verb=f' - {data.nameOfListing} Posted Successfully')
            messages.success(request, f'Posted Successfully')
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request, 'feed/create_post.html', {'form':form})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['description', 'pic', 'tags', 'bid', 'nameOfListing']
    widgets = {
        'description': forms.Textarea(attrs={'rows':150, 'cols':70})
    }
    template_name = 'feed/create_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user== post.user:
        Post.objects.get(pk=pk).delete()
    return redirect('home')


@login_required
def search_posts(request):
    query = request.GET.get('p')
    print('the query: ', query)
    object_list = Post.objects.filter(tags__icontains=query).order_by('-date_posted')

    liked = [i for i in object_list if Like.objects.filter(user = request.user, post=i)]
    context ={
        'posts': object_list,
        'liked_post': liked
    }
    return render(request, "feed/search_posts.html", context)

@login_required
def like(request):
    post_id = request.GET.get("likeId", "")
    user = request.user
    post = Post.objects.get(pk=post_id)
    post.date_added = timezone.now
    liked= False
    like = Like.objects.filter(user=user, post=post)
    if like:
        like.delete()
    else:
        liked = True
        Like.objects.create(user=user, post=post)
    resp = {
        'liked':liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")






