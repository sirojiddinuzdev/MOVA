from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from common.throttles import SearchRateThrottle, ClaimRateThrottle
from .models import Profile, SocialLink, Project, Achievement, CareerTimeline, Media
from .serializers import (
    ProfileSerializer, SocialLinkSerializer, ProjectSerializer, 
    AchievementSerializer, CareerTimelineSerializer, MediaSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # For nested objects, check if user owns the profile
        if hasattr(obj, 'profile'):
            return obj.profile.user == request.user
        # For Profile itself
        return obj.user == request.user

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').prefetch_related(
        'social_links', 'projects', 'achievements', 'career_timeline', 'media'
    )
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_identity_verified', 'is_public_figure', 'location']
    search_fields = ['full_name', 'profession', 'bio', 'location']
    ordering_fields = ['recognition_score', 'created_at']

    def get_throttles(self):
        if self.action == 'list':
            return [SearchRateThrottle()]
        elif self.action == 'claim':
            return [ClaimRateThrottle()]
        return super().get_throttles()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def claim(self, request, pk=None):
        profile = self.get_object()
        
        if profile.is_claimed or profile.user:
            return Response({"error": "Profile is already claimed"}, status=status.HTTP_400_BAD_REQUEST)
            
        from .models import ProfileClaimRequest
        # Check if already has a pending claim
        if ProfileClaimRequest.objects.filter(profile=profile, requester=request.user, status='pending').exists():
            return Response({"error": "You already have a pending claim for this profile."}, status=status.HTTP_400_BAD_REQUEST)
        
        ProfileClaimRequest.objects.create(
            profile=profile,
            requester=request.user,
            method=request.data.get('method', 'api'),
            reason=request.data.get('reason', '')
        )
        
        return Response({"message": f"Claim request submitted for profile: {profile.full_name}"}, status=status.HTTP_200_OK)

class BaseNestedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('profile_pk'))
        if profile.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to add items to this profile.")
        serializer.save(profile=profile)

    def get_queryset(self):
        return self.queryset.filter(profile_id=self.kwargs.get('profile_pk'))

class SocialLinkViewSet(BaseNestedViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer

class ProjectViewSet(BaseNestedViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AchievementViewSet(BaseNestedViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class CareerTimelineViewSet(BaseNestedViewSet):
    queryset = CareerTimeline.objects.all()
    serializer_class = CareerTimelineSerializer

class MediaViewSet(BaseNestedViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
