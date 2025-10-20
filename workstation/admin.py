from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin"""
    list_display = ['username', 'email', 'user_type', 'profile_completeness', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('user_type', 'bio', 'title', 'profile_image',
                       'profile_completeness', 'location', 'website',
                       'linkedin', 'github', 'skills', 'interests')
        }),
    )


class ProjectMembershipInline(admin.TabularInline):
    """Inline for project members"""
    model = ProjectMembership
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project admin"""
    list_display = ['title', 'creator', 'project_type', 'stage', 'status',
                    'views_count', 'is_featured', 'created_at']
    list_filter = ['project_type', 'stage', 'status', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'creator__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags', 'supporters']
    inlines = [ProjectMembershipInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('creator')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin"""
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Skill admin"""
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    """Thought admin"""
    list_display = ['user', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']
    filter_horizontal = ['tags', 'likes']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message admin"""
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['subject', 'content', 'sender__username', 'recipient__username']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'recipient')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Conversation admin"""
    list_display = ['id', 'project', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    filter_horizontal = ['participants']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification admin"""
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'content', 'user__username']


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    """Project update admin"""
    list_display = ['project', 'author', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'content', 'project__title']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('project', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin"""
    list_display = ['user', 'project', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username', 'project__title']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    """Join request admin"""
    list_display = ['user', 'project', 'desired_role', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'project__title', 'message']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'project')


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    """Project membership admin"""
    list_display = ['user', 'project', 'role', 'is_active', 'joined_at']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['user__username', 'project__title']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'project')


@admin.register(AIWorker)
class AIWorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'worker_type', 'is_active', 'created_at']
    list_filter = ['worker_type', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'worker', 'title', 'created_at', 'updated_at']
    list_filter = ['worker', 'created_at']
    search_fields = ['user__username', 'title']
    date_hierarchy = 'created_at'


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'created_at', 'content_preview']
    list_filter = ['sender', 'created_at']
    search_fields = ['content']
    date_hierarchy = 'created_at'

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'


@admin.register(AITool)
class AIToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
