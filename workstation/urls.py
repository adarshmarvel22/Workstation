from django.urls import path
from . import views

urlpatterns = [
    # Home and main pages
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Authentication
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('complete-profile/', views.complete_profile, name='complete_profile'),

    # Projects
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/edit/', views.edit_project, name='edit_project'),
    path('projects/<slug:slug>/support/', views.support_project, name='support_project'),
    path('projects/<slug:slug>/join/', views.join_project, name='join_project'),

    # User profiles
    path('users/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Messages
    path('messages/', views.messages_inbox, name='messages'),
    path('messages/send/<str:username>/', views.send_message, name='send_message'),
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),

    # Thoughts
    path('thoughts/create/', views.create_thought, name='create_thought'),

    # AI Workers URLs
    path('ai-workers/', views.ai_workers_dashboard, name='ai_workers_dashboard'),
    path('ai-workers/<int:worker_id>/', views.ai_conversation, name='ai_conversation'),
    path('ai-workers/<int:worker_id>/<int:conversation_id>/', views.ai_conversation, name='ai_conversation_detail'),
    path('ai-workers/send-message/', views.send_ai_message, name='send_ai_message'),
    path('ai-workers/delete/<int:conversation_id>/', views.delete_conversation, name='delete_ai_conversation'),
]
