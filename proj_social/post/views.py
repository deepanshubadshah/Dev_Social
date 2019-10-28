from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Post, Comment, Notification
from django.contrib.auth.models import User
from .forms import *
from django.template.loader import render_to_string
from django.http import JsonResponse

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
    user = get_object_or_404(User, username=username)
    paginate_by = 5
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {
        'posts': posts,
        'user':user
        }
    return render(request, 'post/user_posts.html', context)


def PostDetailView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')

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
        }
    if request.is_ajax():
        html = render_to_string('post/comments.html', context, request=request)
        return JsonResponse({'form':html})

    return render(request, 'post/post_detail.html', context)


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