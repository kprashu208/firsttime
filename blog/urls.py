from django.urls import path
from .views import (
						PostListView, 
						PostDetailView,
						PostCreateView,
						PostUpdateView,
						PostDeleteView,
						UserPostListView,
						CommentCreateView
					)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('post/<int:pk>/new_comment/', CommentCreateView.as_view(), name='comment-create'),
	path('post/deletecomment/<int:pk>', views.del_comment, name='comment-delete'),
	path('about/', views.about, name='blog-about'),
]