from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.utils import timezone
from .forms import *


def home(request):
    """Landing page"""
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    recent_projects = Project.objects.all()[:9]
    trending_tags = Tag.objects.annotate(
        project_count=Count('projects')
    ).order_by('-project_count')[:10]

    context = {
        'featured_projects': featured_projects,
        'recent_projects': recent_projects,
        'trending_tags': trending_tags,
    }
    return render(request, 'workstation/home.html', context)


def explore(request):
    """Explore page with filters"""
    projects = Project.objects.all()

    # Filters
    user_type = request.GET.get('user_type', '')
    stage = request.GET.get('stage', '')
    status = request.GET.get('status', '')
    tags = request.GET.getlist('tags')
    search = request.GET.get('search', '')

    if user_type:
        projects = projects.filter(creator__user_type=user_type)

    if stage:
        projects = projects.filter(stage=stage)

    if status:
        projects = projects.filter(status=status)

    if tags:
        projects = projects.filter(tags__slug__in=tags).distinct()

    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(short_description__icontains=search)
        )

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    projects = projects.order_by(sort)

    # Pagination
    paginator = Paginator(projects, 12)
    page = request.GET.get('page')
    projects = paginator.get_page(page)

    trending_tags = Tag.objects.annotate(
        project_count=Count('projects')
    ).order_by('-project_count')[:15]

    context = {
        'projects': projects,
        'trending_tags': trending_tags,
        'user_types': User.USER_TYPES,
        'stages': Project.PROJECT_STAGES,
        'statuses': Project.PROJECT_STATUS,
    }
    return render(request, 'workstation/explore.html', context)


@login_required
def project_detail(request, slug):
    """Project detail page"""
    project = get_object_or_404(Project, slug=slug)
    project.views_count += 1
    project.save(update_fields=['views_count'])

    comments = project.comments.filter(parent_comment=None)
    updates = project.updates.all()[:5]
    members = project.projectmembership_set.all()

    is_member = request.user in project.members.all()
    is_supporter = request.user in project.supporters.all()
    has_join_request = JoinRequest.objects.filter(
        user=request.user,
        project=project,
        status='pending'
    ).exists()

    context = {
        'project': project,
        'comments': comments,
        'updates': updates,
        'members': members,
        'is_member': is_member,
        'is_supporter': is_supporter,
        'has_join_request': has_join_request,
    }
    return render(request, 'workstation/project_detail.html', context)


@login_required
def create_project(request):
    """Create new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            form.save_m2m()

            # Add creator as member
            ProjectMembership.objects.create(
                user=request.user,
                project=project,
                role='creator'
            )

            messages.success(request, 'Project created successfully!')
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm()

    context = {'form': form}
    return render(request, 'workstation/create_project.html', context)


@login_required
def edit_project(request, slug):
    """Edit existing project"""
    project = get_object_or_404(Project, slug=slug)

    if project.creator != request.user:
        messages.error(request, 'You do not have permission to edit this project.')
        return redirect('project_detail', slug=slug)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm(instance=project)

    context = {'form': form, 'project': project}
    return render(request, 'workstation/edit_project.html', context)


@login_required
def profile(request, username):
    """User profile page"""
    user = get_object_or_404(User, username=username)
    created_projects = user.created_projects.all()
    joined_projects = user.joined_projects.all()
    supported_projects = user.supported_projects.all()
    recent_thoughts = user.thoughts.all()[:10]

    context = {
        'profile_user': user,
        'created_projects': created_projects,
        'joined_projects': joined_projects,
        'supported_projects': supported_projects,
        'recent_thoughts': recent_thoughts,
    }
    return render(request, 'workstation/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'workstation/edit_profile.html', context)


# @login_required
# def messages_inbox(request):
#     """Messages inbox"""
#     conversations = Conversation.objects.filter(
#         participants=request.user
#     ).select_related('last_message')
#
#     unread_count = Message.objects.filter(
#         recipient=request.user,
#         is_read=False
#     ).count()
#
#     context = {
#         'conversations': conversations,
#         'unread_count': unread_count,
#     }
#     return render(request, 'workstation/messages.html', context)

# @login_required
# def conversation_detail(request, conversation_id):
#     """View conversation"""
#     conversation = get_object_or_404(
#         Conversation,
#         id=conversation_id,
#         participants=request.user
#     )
#
#     messages_list = Message.objects.filter(
#         Q(sender=request.user, recipient__in=conversation.participants.all()) |
#         Q(sender__in=conversation.participants.all(), recipient=request.user)
#     ).order_by('created_at')
#
#     # Mark messages as read
#     messages_list.filter(recipient=request.user, is_read=False).update(is_read=True)
#
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.recipient = conversation.participants.exclude(id=request.user.id).first()
#             message.save()
#
#             conversation.last_message = message
#             conversation.save()
#
#             return redirect('conversation_detail', conversation_id=conversation.id)
#     else:
#         form = MessageForm()
#
#     context = {
#         'conversation': conversation,
#         'messages': messages_list,
#         'form': form,
#     }
#     return render(request, 'workstation/conversation.html', context)


# @login_required
# def send_message(request, username):
#     """Send new message"""
#     recipient = get_object_or_404(User, username=username)
#
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.recipient = recipient
#             message.save()
#
#             # Create or get conversation
#             conversation = Conversation.objects.filter(
#                 participants=request.user
#             ).filter(
#                 participants=recipient
#             ).first()
#
#             if not conversation:
#                 conversation = Conversation.objects.create()
#                 conversation.participants.add(request.user, recipient)
#
#             conversation.last_message = message
#             conversation.save()
#
#             messages.success(request, 'Message sent successfully!')
#             return redirect('conversation_detail', conversation_id=conversation.id)
#     else:
#         form = MessageForm()
#
#     context = {'form': form, 'recipient': recipient}
#     return render(request, 'workstation/send_message.html', context)


# @login_required
# def notifications(request):
#     """User notifications"""
#     notifications = request.user.notifications.all()[:50]
#
#     # Mark as read
#     notifications.filter(is_read=False).update(is_read=True)
#
#     context = {'notifications': notifications}
#     return render(request, 'workstation/notifications.html', context)


@login_required
@require_POST
def support_project(request, slug):
    """Support/unsupport a project"""
    project = get_object_or_404(Project, slug=slug)

    if request.user in project.supporters.all():
        project.supporters.remove(request.user)
        supported = False
    else:
        project.supporters.add(request.user)
        supported = True

        # Create notification
        Notification.objects.create(
            user=project.creator,
            notification_type='support',
            title=f'{request.user.username} supported your project',
            content=f'{request.user.username} is now supporting {project.title}',
            link=f'/projects/{project.slug}/'
        )

    return JsonResponse({
        'success': True,
        'supported': supported,
        'supporters_count': project.supporters.count()
    })


@login_required
@require_POST
def join_project(request, slug):
    """Request to join a project"""
    project = get_object_or_404(Project, slug=slug)
    message = request.POST.get('message', '')
    role = request.POST.get('role', '')

    join_request, created = JoinRequest.objects.get_or_create(
        user=request.user,
        project=project,
        defaults={'message': message, 'desired_role': role}
    )

    if created:
        # Create notification for project creator
        Notification.objects.create(
            user=project.creator,
            notification_type='join_request',
            title=f'{request.user.username} wants to join your project',
            content=message,
            link=f'/projects/{project.slug}/requests/'
        )
        messages.success(request, 'Join request sent!')
    else:
        messages.info(request, 'You already have a pending request.')

    return redirect('project_detail', slug=slug)


# @login_required
# def create_thought(request):
#     """Create a thought/post"""
#     if request.method == 'POST':
#         form = ThoughtForm(request.POST)
#         if form.is_valid():
#             thought = form.save(commit=False)
#             thought.user = request.user
#             thought.save()
#             form.save_m2m()
#             messages.success(request, 'Thought posted!')
#             return redirect('home')
#     else:
#         form = ThoughtForm()
#
#     context = {'form': form}
#     return render(request, 'workstation/create_thought.html', context)


# @login_required
# def dashboard(request):
#     """User dashboard"""
#     my_projects = request.user.created_projects.all()
#     joined_projects = request.user.joined_projects.all()
#     recent_messages = Message.objects.filter(recipient=request.user)[:5]
#     notifications = request.user.notifications.filter(is_read=False)[:10]
#
#     context = {
#         'my_projects': my_projects,
#         'joined_projects': joined_projects,
#         'recent_messages': recent_messages,
#         'notifications': notifications,
#     }
#     return render(request, 'workstation/dashboard.html', context)


def user_register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Workstation Hub!')
            return redirect('home')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'workstation/register.html', context)


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'workstation/login.html')


@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def messages_inbox(request):
    """Messages inbox - list of all conversations"""
    # Get all conversations for the current user
    conversations = Conversation.objects.filter(
        participants=request.user
    ).select_related('last_message').order_by('-updated_at')

    # Count unread messages
    unread_count = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    context = {
        'conversations': conversations,
        'unread_count': unread_count,
    }
    return render(request, 'workstation/messages.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """View a specific conversation and send messages"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    # Get all messages in this conversation
    other_user = conversation.participants.exclude(id=request.user.id).first()

    messages_list = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('created_at')

    # Mark messages as read
    Message.objects.filter(
        recipient=request.user,
        sender=other_user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())

    # Handle new message submission
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            message = Message.objects.create(
                sender=request.user,
                recipient=other_user,
                content=content
            )

            # Update conversation
            conversation.last_message = message
            conversation.updated_at = timezone.now()
            conversation.save()

            # Create notification for recipient
            Notification.objects.create(
                user=other_user,
                notification_type='message',
                title='New message',
                content=f'{request.user.username} sent you a message',
                link=f'/conversations/{conversation.id}/'
            )

            messages.success(request, 'Message sent!')
            return redirect('conversation_detail', conversation_id=conversation.id)
        else:
            messages.error(request, 'Message cannot be empty')

    # Get all conversations for sidebar
    all_conversations = Conversation.objects.filter(
        participants=request.user
    ).select_related('last_message').order_by('-updated_at')

    unread_count = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    context = {
        'conversation': conversation,
        'conversations': all_conversations,
        'messages': messages_list,
        'other_user': other_user,
        'unread_count': unread_count,
    }
    return render(request, 'workstation/messages.html', context)


@login_required
def send_message(request, username):
    """Send a new message to a user"""
    recipient = get_object_or_404(User, username=username)

    if recipient == request.user:
        messages.error(request, "You cannot send a message to yourself")
        return redirect('profile', username=username)

    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            messages.error(request, 'Message content is required')
            return redirect('send_message', username=username)

        # Create the message
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            content=content
        )

        # Get or create conversation
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=recipient
        ).first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, recipient)

        conversation.last_message = message
        conversation.updated_at = timezone.now()
        conversation.save()

        # Create notification
        Notification.objects.create(
            user=recipient,
            notification_type='message',
            title='New message',
            content=f'{request.user.username} sent you a message',
            link=f'/conversations/{conversation.id}/'
        )

        messages.success(request, f'Message sent to {recipient.username}!')
        return redirect('conversation_detail', conversation_id=conversation.id)

    context = {
        'recipient': recipient,
    }
    return render(request, 'workstation/send_message.html', context)


@login_required
def notifications(request):
    """View all notifications"""
    # Get all notifications for the current user
    notifications = request.user.notifications.all().order_by('-created_at')

    # Mark notifications as read when viewed
    notifications.filter(is_read=False).update(is_read=True)

    context = {
        'notifications': notifications,
    }
    return render(request, 'workstation/notifications.html', context)


@login_required
def create_thought(request):
    """Create a new thought/post"""
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            form.save_m2m()  # Save the many-to-many tags

            messages.success(request, 'Thought posted successfully!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = ThoughtForm()

    context = {
        'form': form,
    }
    return render(request, 'workstation/create_thought.html', context)


@login_required
def dashboard(request):
    """User dashboard with overview"""
    # Get user's projects
    my_projects = request.user.created_projects.all().order_by('-created_at')[:5]

    # Get projects user has joined
    joined_projects = request.user.joined_projects.exclude(
        id__in=my_projects.values_list('id', flat=True)
    ).order_by('-projectmembership__joined_at')[:5]

    # Get recent messages
    recent_messages = Message.objects.filter(
        recipient=request.user
    ).select_related('sender').order_by('-created_at')[:5]

    # Get unread notifications
    unread_notifications = request.user.notifications.filter(
        is_read=False
    ).order_by('-created_at')[:10]

    # Get stats
    stats = {
        'projects_created': request.user.created_projects.count(),
        'projects_joined': request.user.joined_projects.count(),
        'projects_supported': request.user.supported_projects.count(),
        'unread_messages': Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).count(),
        'unread_notifications': unread_notifications.count(),
    }

    # Get recent activity (join requests, comments, etc.)
    recent_join_requests = JoinRequest.objects.filter(
        project__creator=request.user,
        status='pending'
    ).select_related('user', 'project').order_by('-created_at')[:5]

    context = {
        'my_projects': my_projects,
        'joined_projects': joined_projects,
        'recent_messages': recent_messages,
        'notifications': unread_notifications,
        'stats': stats,
        'join_requests': recent_join_requests,
    }
    return render(request, 'workstation/dashboard.html', context)


# API endpoint for marking notifications as read
@login_required
def mark_notification_read(request, notification_id):
    """Mark a single notification as read"""
    if request.method == 'POST':
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user
        )
        notification.is_read = True
        notification.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


# API endpoint for marking all notifications as read
@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    if request.method == 'POST':
        count = request.user.notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({'success': True, 'count': count})
    return JsonResponse({'success': False}, status=400)


# API endpoint for deleting a message
@login_required
def delete_message(request, message_id):
    """Delete a message"""
    if request.method == 'POST':
        message = get_object_or_404(
            Message,
            Q(id=message_id) & (Q(sender=request.user) | Q(recipient=request.user))
        )
        message.delete()
        messages.success(request, 'Message deleted')
        return redirect('messages')
    return redirect('messages')


# API endpoint for deleting a conversation
@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    if request.method == 'POST':
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=request.user
        )

        # Delete all messages in this conversation
        other_user = conversation.participants.exclude(id=request.user.id).first()
        Message.objects.filter(
            Q(sender=request.user, recipient=other_user) |
            Q(sender=other_user, recipient=request.user)
        ).delete()

        conversation.delete()
        messages.success(request, 'Conversation deleted')
        return redirect('messages')
    return redirect('messages')


# Helper function to create a conversation between two users
def get_or_create_conversation(user1, user2):
    """Get existing conversation or create new one"""
    conversation = Conversation.objects.filter(
        participants=user1
    ).filter(
        participants=user2
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(user1, user2)

    return conversation
