from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers
from todo_app.models import Task, UserProfile

from todo_app.models import TelegramUser

from todo_app.models import TaskCategory


class TaskCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)
    username = serializers.CharField(write_only=True)
    class Meta:
        model = Task
        fields = ('username', 'telegram_id','title', 'category', 'description', 'due_date', 'is_completed')

    def create(self, validated_data):

        telegram_id = validated_data.pop('telegram_id')
        username = validated_data.pop('username')
        user = None

        if telegram_id is not None:
            standart_username = username or f'tg_user_{telegram_id}'
            try:
                user, created = TelegramUser.objects.get_or_create(
                    telegram_id=telegram_id,
                    defaults={'username': standart_username,
                        'telegram_username': username,
                              'password': '!',
                              }
                )
                if not created and user.telegram_username != username:
                    user.telegram_username = username
                    user.save(update_fields=['telegram_username', 'username', ])
            except IntegrityError:
                    raise serializers.ValidationError(
                        {"telegram_id": "Ошибка: Пользователь с таким ID или именем уже существует."})
            except Exception as e:
                raise serializers.ValidationError({"non_field_errors": f"Внутренняя ошибка пользователя: {e}"})

            if user is None:
                raise serializers.ValidationError({"user": "Ошибка: Объект пользователя не был определен."})

            category_name = validated_data.pop('category')
            try:
                category_obj = TaskCategory.objects.get(name=category_name)
            except TaskCategory.DoesNotExist:
                raise serializers.ValidationError({"category": "Ошибка"})

            validated_data['user'] = user
            validated_data['category'] = category_obj

            return Task.objects.create(**validated_data)


    def create(self, validated_data):
        telegram_id = validated_data.pop('telegram_id')

        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            user_obj = user_profile.user
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({'telegram_id': 'User does not found'})

        validated_data['user'] = user_obj
        return Task.objects.create(**validated_data)


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'