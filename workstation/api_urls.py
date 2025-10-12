from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'projects', api_views.ProjectViewSet)
router.register(r'users', api_views.UserViewSet)
router.register(r'thoughts', api_views.ThoughtViewSet)
router.register(r'messages', api_views.MessageViewSet, basename='message')
router.register(r'notifications', api_views.NotificationViewSet, basename='notification')
router.register(r'comments', api_views.CommentViewSet, basename='comment')
router.register(r'join-requests', api_views.JoinRequestViewSet, basename='joinrequest')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Custom endpoints
    path('stats/', api_views.api_stats, name='api-stats'),
    path('dashboard/', api_views.dashboard_data, name='api-dashboard'),

    # Auth endpoints (if using Django REST Framework auth)
    path('auth/', include('rest_framework.urls')),
]
