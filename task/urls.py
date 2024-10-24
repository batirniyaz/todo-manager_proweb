from django.urls import path

from .views import TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('', TaskListAPIView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
]