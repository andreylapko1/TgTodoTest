from .core.fields import CustomPKFields
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    id = CustomPKFields(max_length=35, primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100, null=False, )
    category = models.ForeignKey('TaskCategory', on_delete=models.CASCADE, related_name='tasks_by_category')
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskCategory(models.Model):

    id = CustomPKFields(max_length=35, primary_key=True)
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "TaskCategories"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    telegram_id = models.BigIntegerField(unique=True, db_index=True)

    def __str__(self):
        return self.user.username

# Create your models here.
