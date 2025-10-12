from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Extended user model for Workstation Hub"""
    USER_TYPES = (
        ('founder', 'Founder'),
        ('professional', 'Professional'),
        ('student', 'Student'),
        ('enthusiast', 'Tech Enthusiast'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='enthusiast')
    bio = models.TextField(blank=True)
    title = models.CharField(max_length=200, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    profile_completeness = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    skills = models.ManyToManyField('Skill', blank=True, related_name='users')
    interests = models.ManyToManyField('Tag', blank=True, related_name='interested_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class Tag(models.Model):
    """Tags for categorizing projects and ideas"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        ordering = ['name']


class Skill(models.Model):
    """Skills for users"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'skills'
        ordering = ['name']


class Project(models.Model):
    """Projects/Ideas/Ventures on the platform"""
    PROJECT_STAGES = (
        ('idea', 'Idea'),
        ('prototype', 'Prototype'),
        ('mvp', 'MVP'),
        ('growth', 'Growth'),
        ('mature', 'Mature'),
    )

    PROJECT_STATUS = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('paused', 'Paused'),
    )

    PROJECT_TYPES = (
        ('project', 'Project'),
        ('idea', 'Idea'),
        ('venture', 'Venture'),
    )

    COLLABORATION_TYPES = (
        ('co-founders', 'Co-founders'),
        ('mentors', 'Mentors'),
        ('investors', 'Investors'),
        ('contributors', 'Contributors'),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='project')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    stage = models.CharField(max_length=20, choices=PROJECT_STAGES, default='idea')
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='open')
    collaboration_needed = models.CharField(max_length=20, choices=COLLABORATION_TYPES, blank=True)
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')
    members = models.ManyToManyField(User, through='ProjectMembership', related_name='joined_projects')
    supporters = models.ManyToManyField(User, blank=True, related_name='supported_projects')
    views_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.short_description and self.description:
            self.short_description = self.description[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']


class ProjectMembership(models.Model):
    """Through model for project members"""
    ROLES = (
        ('creator', 'Creator'),
        ('co-founder', 'Co-founder'),
        ('member', 'Member'),
        ('contributor', 'Contributor'),
        ('mentor', 'Mentor'),
        ('investor', 'Investor'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'project_memberships'
        unique_together = ('user', 'project')


class Thought(models.Model):
    """Quick thoughts/posts by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thoughts')
    content = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag, blank=True, related_name='thoughts')
    likes = models.ManyToManyField(User, blank=True, related_name='liked_thoughts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"

    class Meta:
        db_table = 'thoughts'
        ordering = ['-created_at']


class Message(models.Model):
    """Messages between users"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}"

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']


class Conversation(models.Model):
    """Conversation threads between users"""
    participants = models.ManyToManyField(User, related_name='conversations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='conversations')
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']


class Notification(models.Model):
    """Notifications for users"""
    NOTIFICATION_TYPES = (
        ('message', 'New Message'),
        ('project_invite', 'Project Invitation'),
        ('support', 'New Support'),
        ('join_request', 'Join Request'),
        ('mention', 'Mention'),
        ('comment', 'Comment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']


class ProjectUpdate(models.Model):
    """Updates posted by project creators"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_updates'
        ordering = ['-created_at']


class Comment(models.Model):
    """Comments on projects"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']


class JoinRequest(models.Model):
    """Requests to join projects"""
    REQUEST_STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='join_requests')
    message = models.TextField()
    desired_role = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'join_requests'
        unique_together = ('user', 'project')
        ordering = ['-created_at']
