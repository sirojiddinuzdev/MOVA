from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_identity_verified', 'is_public_figure', 'location']
    search_fields = ['full_name', 'profession', 'bio', 'location']
    ordering_fields = ['recognition_score', 'created_at']

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def claim(self, request, pk=None):
        profile = self.get_object()
        
        if profile.is_claimed:
            return Response({"error": "Profile is already claimed"}, status=status.HTTP_400_BAD_REQUEST)
            
        profile.user = request.user
        profile.is_claimed = True
        profile.is_identity_verified = True
        profile.save()
        
        return Response({"message": f"Successfully claimed profile: {profile.full_name}"}, status=status.HTTP_200_OK)

class BaseNestedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('profile_pk'))
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
