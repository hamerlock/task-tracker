from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
]