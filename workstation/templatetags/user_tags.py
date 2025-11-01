from django import template

register = template.Library()

@register.filter
def is_following(user, target_user):
    """Check if user is following target_user"""
    if not user.is_authenticated:
        return False
    return user.following.filter(pk=target_user.pk).exists()

@register.filter
def has_pending_request(user, target_user):
    """Check if there's a pending connection request"""
    if not user.is_authenticated:
        return False
    from workstation.models import ConnectionRequest
    return ConnectionRequest.objects.filter(
        from_user=user,
        to_user=target_user,
        status='pending'
    ).exists()
