from rest_framework import serializers
from .models import Profile, SocialLink, Project, Achievement, CareerTimeline, Media

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'
        read_only_fields = ('profile',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('profile',)

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
        read_only_fields = ('profile',)

class CareerTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerTimeline
        fields = '__all__'
        read_only_fields = ('profile',)

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = ('profile',)

class ProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    career_timeline = CareerTimelineSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'is_identity_verified', 'is_public_figure', 'is_claimed', 'recognition_score')
