from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class UserActivityMiddleware(MiddlewareMixin):
    """Track user last activity"""

    def process_request(self, request):
        if request.user.is_authenticated:
            # Update last activity timestamp
            User.objects.filter(pk=request.user.pk).update(
                last_login=timezone.now()
            )
        return None


class ProjectViewCountMiddleware(MiddlewareMixin):
    """Increment project view count (handled in view instead for better control)"""
    pass


class APIUsageMiddleware(MiddlewareMixin):
    """Track API usage for rate limiting"""

    def process_request(self, request):
        if request.path.startswith('/api/'):
            # Could implement rate limiting logic here
            pass
        return None
