from rest_framework import serializers

from todo_app.models import TaskCategory


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ('name', 'id')