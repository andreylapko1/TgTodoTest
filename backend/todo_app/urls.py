from todo_app.views.task_views import TaskCreateView, TaskListView, TaskUpdateDestroyView
from todo_app.views.category_views import CategoryListView
from django.urls import path

urlpatterns = [
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>', TaskUpdateDestroyView.as_view(), name='task_upd_del'),
    path('categories/', CategoryListView.as_view(), name='category_list')
]