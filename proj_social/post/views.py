from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Post, Comment, Notification
from django.contrib.auth.models import User
from .forms import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from users.models import Friend

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'post/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'    # PostListView looks for <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

def PostListView(request):
    posts = Post.objects.order_by('-date_posted')
    notifications = Notification.objects.order_by('-id')[:5]
    context = {
        'posts': posts,
        'notifications':notifications
        }
    return render(request, 'post/home.html', context)


def UserPostListView(request, username):
    userp = get_object_or_404(User, username=username)
    paginate_by = 5
    posts = Post.objects.filter(author=userp).order_by('-date_posted')
    notifications = Notification.objects.order_by('-id')[:5]
    obj_exist = Friend.objects.filter(current_user=userp).exists()
    if obj_exist:
        user_connections = Friend.objects.get(current_user=userp)
        newuser_sent = user_connections.users.filter(username=request.user.username).exists()
    else:
        newuser_sent = False

    sent_requests_c = Friend.objects.filter(current_user=request.user.id).exists()
    if sent_requests_c:
        sent_requests = Friend.objects.get(current_user=request.user.id)
        is_sent = sent_requests.users.filter(username=username).exists()
    else:
        is_sent = False

    context = {
        'posts': posts,
        'userp':userp,
        'notifications':notifications,
        'is_sent': is_sent,
        'newuser_sent': newuser_sent,
        }
    return render(request, 'post/user_posts.html', context)


def PostDetailView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    notifications = Notification.objects.order_by('-id')[:5]
    is_liked=False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, author=request.user, content=content, reply=comment_qs)
            comment.save()
            #return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'notifications': notifications,
        'total_likes': post.total_likes(),
        }
    if request.is_ajax():
        html = render_to_string('post/comments.html', context, request=request)
        return JsonResponse({'form':html})

    return render(request, 'post/post_detail.html', context)

#post detail page like option
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    notifications = Notification.objects.order_by('-id')[:5]
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'notifications': notifications,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('post/likes.html', context, request=request)
        return JsonResponse({'form':html})

#main page like option
def mlike_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    notifications = Notification.objects.order_by('-id')[:5]
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    context = {
        'post': post,
        'notifications': notifications
        }
    if request.is_ajax():
        html = render_to_string('post/mlikes.html', context, request=request)
        return JsonResponse({'form':html})

#profile page like option
def plike_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    notifications = Notification.objects.order_by('-id')[:5]
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    context = {
        'post': post,
        'notifications': notifications
        }
    if request.is_ajax():
        html = render_to_string('post/plikes.html', context, request=request)
        return JsonResponse({'form':html})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'post/about.html', {'title': 'About'})
