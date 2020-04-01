from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new_post/', views.new_post, name='new_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_pk>/', views.post_detail),
    path('update_post/<int:post_pk>/', views.update_post),
    path('update_post/<int:post_pk>/complete/', views.update_post_complete),
    path('delete/<int:post_pk>/', views.delete_post),
]