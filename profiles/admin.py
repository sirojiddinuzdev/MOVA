from django.contrib import admin
from .models import Profile, SocialLink, Project, Achievement, CareerTimeline, Media

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1

class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1

class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1

class CareerTimelineInline(admin.TabularInline):
    model = CareerTimeline
    extra = 1

class MediaInline(admin.TabularInline):
    model = Media
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'profession', 'recognition_score', 'is_identity_verified', 'is_public_figure', 'is_claimed')
    list_filter = ('is_identity_verified', 'is_public_figure', 'is_claimed')
    search_fields = ('full_name', 'profession', 'location')
    inlines = [SocialLinkInline, ProjectInline, AchievementInline, CareerTimelineInline, MediaInline]

admin.site.register(SocialLink)
admin.site.register(Project)
admin.site.register(Achievement)
admin.site.register(CareerTimeline)
admin.site.register(Media)
