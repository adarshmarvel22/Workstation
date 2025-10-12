from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'user_type', 'bio', 'title', 'profile_image',
                  'profile_completeness', 'location', 'created_at']
        read_only_fields = ['id', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer"""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class SkillSerializer(serializers.ModelSerializer):
    """Skill serializer"""

    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class ProjectListSerializer(serializers.ModelSerializer):
    """Project list serializer (simplified)"""
    creator = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    supporters_count = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'short_description', 'project_type',
                  'stage', 'status', 'cover_image', 'creator', 'tags',
                  'supporters_count', 'members_count', 'views_count', 'created_at']

    def get_supporters_count(self, obj):
        return obj.supporters.count()

    def get_members_count(self, obj):
        return obj.members.count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Project detail serializer (full)"""
    creator = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    supporters = UserSerializer(many=True, read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_members_count(self, obj):
        return obj.members.count()


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Project creation serializer"""

    class Meta:
        model = Project
        fields = ['title', 'short_description', 'description', 'project_type',
                  'stage', 'status', 'collaboration_needed', 'cover_image', 'tags']


class ThoughtSerializer(serializers.ModelSerializer):
    """Thought serializer"""
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Thought
        fields = ['id', 'user', 'content', 'tags', 'likes_count', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer"""
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'subject', 'content',
                  'is_read', 'created_at', 'read_at']
        read_only_fields = ['id', 'created_at', 'read_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer"""

    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'content', 'link',
                  'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'project', 'content', 'parent_comment',
                  'replies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class JoinRequestSerializer(serializers.ModelSerializer):
    """Join request serializer"""
    user = UserSerializer(read_only=True)
    project = ProjectListSerializer(read_only=True)

    class Meta:
        model = JoinRequest
        fields = ['id', 'user', 'project', 'message', 'desired_role',
                  'status', 'created_at', 'responded_at']
        read_only_fields = ['id', 'created_at', 'responded_at']


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Project update serializer"""
    author = UserSerializer(read_only=True)

    class Meta:
        model = ProjectUpdate
        fields = ['id', 'project', 'author', 'title', 'content',
                  'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProjectMembershipSerializer(serializers.ModelSerializer):
    """Project membership serializer"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'project', 'role', 'is_active', 'joined_at']
        read_only_fields = ['id', 'joined_at']
        