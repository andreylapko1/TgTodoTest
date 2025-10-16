from  todo_app.mixins import QuerySetCustomMixin
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView
from todo_app.serializers.task_serializers import TaskCreateSerializer, TaskListSerializer
from  todo_app.models import Task



class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer





class TaskListView(ListAPIView, QuerySetCustomMixin):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer



class TaskUpdateDestroyView(RetrieveUpdateDestroyAPIView, QuerySetCustomMixin):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer




# Create your views here.
