from .models import Task, UserProfile


class QuerySetCustomMixin:
    def get_queryset(self):
        telegram_id = self.request.query_params.get('telegram_id')
        if not telegram_id:
            return self.queryset.none()
        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            user_obj = user_profile.user
            return self.queryset.filter(user=user_obj).order_by('-created_at')

        except UserProfile.DoesNotExist:
            return self.queryset.none()