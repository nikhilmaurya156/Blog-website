from django.urls import path
from . import views
from .views import (PostListView, PostCreateView,PostUpdateView,PostDetailUpdateView,FieldPostListView,
                    PostComment,PostDeleteView, UserPostListView, SuggestionCreateView,
                   PostDetailView,PostCreateAddView, PostDetailDeleteView, CommmentDeleteView)


urlpatterns = [
    path('post/suggestion/', SuggestionCreateView.as_view(), name='suggestion'),
    path('post/search/', views.autocompleteModel, name='search'),
    path('', PostListView.as_view(), name='blog_home'),
    path('comment/<slug:slug>/', PostComment.as_view(), name='comment'),
    path('bookmark/<slug:b_title>/<slug:b_author>', views.bookmark, name='bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('com/<int:pk>/', views.submit, name='post_comment'),
    path('about/', views.about, name='blog_about'),
    path('post/detail/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new/add/<slug:slug>/', PostCreateAddView.as_view(), name='post-create-add'), 
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/<int:pk>/update/', PostDetailUpdateView.as_view(), name='post-detail-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<slug:slug>/<int:pk>/delete/', PostDetailDeleteView.as_view(), name='post-detail-delete'),
    path('comment/<slug:slug>/<int:pk>/delete/', CommmentDeleteView.as_view(), name='comment-delete'),
    path('user/<slug:slug>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<slug:slug>/', FieldPostListView.as_view(), name='user-field-posts'),
    path('post/<slug:slug>/likes', views.likes, name='user-posts-likes')
]
