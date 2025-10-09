from django.contrib import admin

from .models import Task, TaskCategory


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskCategory)
class CategoryAdmin(admin.ModelAdmin):
    pass



# Register your models here.
