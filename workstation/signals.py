from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from .models import *


@receiver(post_save, sender=User)
def calculate_profile_completeness(sender, instance, created, **kwargs):
    """Calculate profile completeness percentage"""
    if not created:  # Only for updates, not creation
        completeness = 0
        fields = [
            (instance.first_name, 10),
            (instance.last_name, 10),
            (instance.bio, 15),
            (instance.title, 10),
            (instance.profile_image, 15),
            (instance.location, 10),
            (instance.website or instance.linkedin or instance.github, 10),
        ]

        for field, weight in fields:
            if field:
                completeness += weight

        # Check skills and interests
        if instance.skills.count() > 0:
            completeness += 10
        if instance.interests.count() > 0:
            completeness += 10

        if instance.profile_completeness != completeness:
            User.objects.filter(pk=instance.pk).update(profile_completeness=completeness)


@receiver(post_save, sender=ProjectMembership)
def notify_user_added_to_project(sender, instance, created, **kwargs):
    """Notify user when added to a project"""
    if created and instance.user != instance.project.creator:
        Notification.objects.create(
            user=instance.user,
            notification_type='project_invite',
            title='Added to project',
            content=f'You have been added to {instance.project.title} as {instance.role}',
            link=f'/projects/{instance.project.slug}/'
        )


@receiver(post_save, sender=Comment)
def notify_project_creator_of_comment(sender, instance, created, **kwargs):
    """Notify project creator when someone comments"""
    if created and instance.user != instance.project.creator:
        Notification.objects.create(
            user=instance.project.creator,
            notification_type='comment',
            title='New comment on your project',
            content=f'{instance.user.username} commented on {instance.project.title}',
            link=f'/projects/{instance.project.slug}/#comments'
        )


@receiver(post_save, sender=Message)
def notify_user_of_new_message(sender, instance, created, **kwargs):
    """Notify user of new message"""
    if created:
        Notification.objects.create(
            user=instance.recipient,
            notification_type='message',
            title='New message',
            content=f'You have a new message from {instance.sender.username}',
            link='/messages/'
        )


@receiver(post_save, sender=Thought)
def notify_mentioned_users(sender, instance, created, **kwargs):
    """Notify users mentioned in thoughts (if @username is used)"""
    if created:
        import re
        # Find @mentions in the content
        mentions = re.findall(r'@(\w+)', instance.content)

        for username in set(mentions):  # Remove duplicates
            try:
                user = User.objects.get(username=username)
                if user != instance.user:
                    Notification.objects.create(
                        user=user,
                        notification_type='mention',
                        title='You were mentioned',
                        content=f'{instance.user.username} mentioned you in a thought',
                        link=f'/users/{instance.user.username}/'
                    )
            except User.DoesNotExist:
                pass


@receiver(post_save, sender=ProjectUpdate)
def notify_project_supporters_of_update(sender, instance, created, **kwargs):
    """Notify project supporters and members when an update is posted"""
    if created:
        # Get all supporters and members
        users_to_notify = set(instance.project.supporters.all()) | set(instance.project.members.all())
        users_to_notify.discard(instance.author)  # Don't notify the author

        for user in users_to_notify:
            Notification.objects.create(
                user=user,
                notification_type='comment',  # Using comment type for updates
                title=f'New update from {instance.project.title}',
                content=instance.title,
                link=f'/projects/{instance.project.slug}/#updates'
            )


@receiver(pre_save, sender=Project)
def update_project_slug_if_title_changed(sender, instance, **kwargs):
    """Update slug if title changes"""
    if instance.pk:
        try:
            old_instance = Project.objects.get(pk=instance.pk)
            if old_instance.title != instance.title:
                from django.utils.text import slugify
                base_slug = slugify(instance.title)
                slug = base_slug
                counter = 1

                # Ensure unique slug
                while Project.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                instance.slug = slug
        except Project.DoesNotExist:
            pass


@receiver(m2m_changed, sender=Project.supporters.through)
def update_support_count(sender, instance, action, **kwargs):
    """Could be used to cache supporter count if needed"""
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Update cached count or trigger other actions
        pass


# Signal to mark messages as read when conversation is opened
@receiver(post_save, sender=Message)
def mark_conversation_messages_read(sender, instance, created, **kwargs):
    """Mark messages in a conversation as read when user opens it"""
    # This would be better handled in the view, but kept here as example
    pass
