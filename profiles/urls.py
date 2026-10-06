from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    ProfileViewSet, SocialLinkViewSet, ProjectViewSet, 
    AchievementViewSet, CareerTimelineViewSet, MediaViewSet
)

router = routers.SimpleRouter()
router.register(r'', ProfileViewSet, basename='profile')

profile_router = routers.NestedSimpleRouter(router, r'', lookup='profile')
profile_router.register(r'social_links', SocialLinkViewSet, basename='profile-social-links')
profile_router.register(r'projects', ProjectViewSet, basename='profile-projects')
profile_router.register(r'achievements', AchievementViewSet, basename='profile-achievements')
profile_router.register(r'timeline', CareerTimelineViewSet, basename='profile-timeline')
profile_router.register(r'media', MediaViewSet, basename='profile-media')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(profile_router.urls)),
]
