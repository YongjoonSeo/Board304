from django.urls import path
from . import views

app_name = 'normalboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comments/', views.create_comments, name='create_comments'),
    path('<int:pk>/comments/<int:comment_pk>/delete/', views.delete_comments, name='delete_comments'),
]