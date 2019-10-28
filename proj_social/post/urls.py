from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    #path('', views.home, name='post-home'),                   # Will us this for customized feed
    path('', views.PostListView, name='post-home'),       # As PostListView is a class not view
    path('user/<str:username>', views.UserPostListView, name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='post-about'),
]



# PostListView looks for <app>/<model>_<viewtype>.html
