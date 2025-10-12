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


@login_required
def messages_inbox(request):
    """Messages inbox"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).select_related('last_message')

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
    """View conversation"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    messages_list = Message.objects.filter(
        Q(sender=request.user, recipient__in=conversation.participants.all()) |
        Q(sender__in=conversation.participants.all(), recipient=request.user)
    ).order_by('created_at')

    # Mark messages as read
    messages_list.filter(recipient=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = conversation.participants.exclude(id=request.user.id).first()
            message.save()

            conversation.last_message = message
            conversation.save()

            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    context = {
        'conversation': conversation,
        'messages': messages_list,
        'form': form,
    }
    return render(request, 'workstation/conversation.html', context)


@login_required
def send_message(request, username):
    """Send new message"""
    recipient = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()

            # Create or get conversation
            conversation = Conversation.objects.filter(
                participants=request.user
            ).filter(
                participants=recipient
            ).first()

            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, recipient)

            conversation.last_message = message
            conversation.save()

            messages.success(request, 'Message sent successfully!')
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    context = {'form': form, 'recipient': recipient}
    return render(request, 'workstation/send_message.html', context)


@login_required
def notifications(request):
    """User notifications"""
    notifications = request.user.notifications.all()[:50]

    # Mark as read
    notifications.filter(is_read=False).update(is_read=True)

    context = {'notifications': notifications}
    return render(request, 'workstation/notifications.html', context)


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


@login_required
def create_thought(request):
    """Create a thought/post"""
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            form.save_m2m()
            messages.success(request, 'Thought posted!')
            return redirect('home')
    else:
        form = ThoughtForm()

    context = {'form': form}
    return render(request, 'workstation/create_thought.html', context)


@login_required
def dashboard(request):
    """User dashboard"""
    my_projects = request.user.created_projects.all()
    joined_projects = request.user.joined_projects.all()
    recent_messages = Message.objects.filter(recipient=request.user)[:5]
    notifications = request.user.notifications.filter(is_read=False)[:10]

    context = {
        'my_projects': my_projects,
        'joined_projects': joined_projects,
        'recent_messages': recent_messages,
        'notifications': notifications,
    }
    return render(request, 'workstation/dashboard.html', context)


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
