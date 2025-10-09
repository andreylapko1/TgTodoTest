from rest_framework import serializers
from todo_app.models import Task, UserProfile



class TaskCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Task
        fields = ('telegram_id','title', 'category', 'description', 'due_date', 'is_completed')


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