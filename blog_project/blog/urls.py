from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PostListView

urlpatterns = [
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('', PostListView.as_view(), name='post_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/posts/', views.post_review_list, name='post_review_list'),
    path('admin/posts/<int:pk>/<str:action>', views.post_review, name='post_review'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]