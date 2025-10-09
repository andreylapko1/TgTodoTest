from  todo_app.mixins import QuerySetCustomMixin
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView
from todo_app.models import TaskCategory
from todo_app.serializers.category_serializers import CategoryCreateSerializer


class CategoryListView(ListAPIView):
    queryset = TaskCategory.objects.all()
    serializer_class = CategoryCreateSerializer
