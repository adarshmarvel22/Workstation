from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProjectViewSet(viewsets.ModelViewSet):
    """API viewset for projects"""
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project_type', 'stage', 'status', 'creator__user_type']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'views_count', 'title']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'create':
            return ProjectCreateSerializer
        return ProjectDetailSerializer

    def perform_create(self, serializer):
        project = serializer.save(creator=self.request.user)
        # Add creator as member
        ProjectMembership.objects.create(
            user=self.request.user,
            project=project,
            role='creator'
        )

    @action(detail=True, methods=['post'])
    def support(self, request, slug=None):
        """Support/unsupport a project"""
        project = self.get_object()

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

        return Response({
            'supported': supported,
            'supporters_count': project.supporters.count()
        })

    @action(detail=True, methods=['post'])
    def join(self, request, slug=None):
        """Request to join a project"""
        project = self.get_object()
        message = request.data.get('message', '')
        role = request.data.get('desired_role', '')

        join_request, created = JoinRequest.objects.get_or_create(
            user=request.user,
            project=project,
            defaults={'message': message, 'desired_role': role}
        )

        if created:
            Notification.objects.create(
                user=project.creator,
                notification_type='join_request',
                title=f'{request.user.username} wants to join your project',
                content=message,
                link=f'/projects/{project.slug}/requests/'
            )
            return Response({'status': 'request_sent'}, status=status.HTTP_201_CREATED)

        return Response({'status': 'already_requested'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def members(self, request, slug=None):
        """Get project members"""
        project = self.get_object()
        memberships = project.projectmembership_set.all()
        serializer = ProjectMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def updates(self, request, slug=None):
        """Get project updates"""
        project = self.get_object()
        updates = project.updates.all()
        serializer = ProjectUpdateSerializer(updates, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        """Get project comments"""
        project = self.get_object()
        comments = project.comments.filter(parent_comment=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'bio']

    @action(detail=True, methods=['get'])
    def projects(self, request, username=None):
        """Get user's projects"""
        user = self.get_object()
        projects = user.created_projects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def thoughts(self, request, username=None):
        """Get user's thoughts"""
        user = self.get_object()
        thoughts = user.thoughts.all()[:20]
        serializer = ThoughtSerializer(thoughts, many=True)
        return Response(serializer.data)


class ThoughtViewSet(viewsets.ModelViewSet):
    """API viewset for thoughts"""
    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like/unlike a thought"""
        thought = self.get_object()

        if request.user in thought.likes.all():
            thought.likes.remove(request.user)
            liked = False
        else:
            thought.likes.add(request.user)
            liked = True

        return Response({
            'liked': liked,
            'likes_count': thought.likes.count()
        })


class MessageViewSet(viewsets.ModelViewSet):
    """API viewset for messages"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Message.objects.filter(
            recipient=self.request.user
        ) | Message.objects.filter(
            sender=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get inbox messages"""
        messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
        page = self.paginate_queryset(messages)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get sent messages"""
        messages = Message.objects.filter(sender=request.user).order_by('-created_at')
        page = self.paginate_queryset(messages)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        if message.recipient == request.user:
            message.is_read = True
            message.save()
            return Response({'status': 'marked_read'})
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'marked_read': count})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked_read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notification count"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})


class CommentViewSet(viewsets.ModelViewSet):
    """API viewset for comments"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        project_slug = self.request.query_params.get('project', None)
        if project_slug:
            return Comment.objects.filter(
                project__slug=project_slug,
                parent_comment=None
            )
        return Comment.objects.filter(parent_comment=None)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JoinRequestViewSet(viewsets.ModelViewSet):
    """API viewset for join requests"""
    serializer_class = JoinRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show requests user has made or received (if creator)
        return JoinRequest.objects.filter(
            user=self.request.user
        ) | JoinRequest.objects.filter(
            project__creator=self.request.user
        )

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a join request"""
        join_request = self.get_object()

        if join_request.project.creator != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        join_request.status = 'accepted'
        join_request.responded_at = timezone.now()
        join_request.save()

        # Add user to project
        ProjectMembership.objects.create(
            user=join_request.user,
            project=join_request.project,
            role='member'
        )

        # Notify user
        Notification.objects.create(
            user=join_request.user,
            notification_type='join_request',
            title='Join request accepted',
            content=f'Your request to join {join_request.project.title} was accepted!',
            link=f'/projects/{join_request.project.slug}/'
        )

        return Response({'status': 'accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a join request"""
        join_request = self.get_object()

        if join_request.project.creator != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        join_request.status = 'rejected'
        join_request.responded_at = timezone.now()
        join_request.save()

        return Response({'status': 'rejected'})


@api_view(['GET'])
def api_stats(request):
    """Get platform statistics"""
    stats = {
        'total_projects': Project.objects.count(),
        'total_users': User.objects.count(),
        'total_thoughts': Thought.objects.count(),
        'active_projects': Project.objects.filter(status='open').count(),
        'project_stages': {
            'idea': Project.objects.filter(stage='idea').count(),
            'prototype': Project.objects.filter(stage='prototype').count(),
            'mvp': Project.objects.filter(stage='mvp').count(),
            'growth': Project.objects.filter(stage='growth').count(),
            'mature': Project.objects.filter(stage='mature').count(),
        },
        'user_types': {
            'founders': User.objects.filter(user_type='founder').count(),
            'professionals': User.objects.filter(user_type='professional').count(),
            'students': User.objects.filter(user_type='student').count(),
            'enthusiasts': User.objects.filter(user_type='enthusiast').count(),
        }
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """Get user dashboard data"""
    user = request.user

    data = {
        'profile': UserSerializer(user).data,
        'my_projects': ProjectListSerializer(user.created_projects.all()[:5], many=True).data,
        'joined_projects': ProjectListSerializer(user.joined_projects.all()[:5], many=True).data,
        'supported_projects': ProjectListSerializer(user.supported_projects.all()[:5], many=True).data,
        'unread_messages': Message.objects.filter(recipient=user, is_read=False).count(),
        'unread_notifications': Notification.objects.filter(user=user, is_read=False).count(),
        'recent_thoughts': ThoughtSerializer(user.thoughts.all()[:5], many=True).data,
    }

    return Response(data)
