from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from profiles.models import Project, Achievement, Media, Profile
from reputation.models import ScoreMetric

from django.db.models import Avg
from reviews.models import Review

def recalculate_metrics(profile):
    metric, created = ScoreMetric.objects.get_or_create(profile=profile)
    
    # Calculate Projects Score (max 100)
    projects_count = profile.projects.count()
    metric.projects_score = min(projects_count * 10, 100)

    # Calculate Achievements Score
    achievements_count = profile.achievements.count()
    metric.achievements_score = min(achievements_count * 15, 100)

    # Calculate Media Presence Score
    media_count = profile.media_files.count()
    metric.media_presence_score = min(media_count * 5, 100)

    # Calculate Audience Score based on reviews
    avg_rating = Review.objects.filter(reviewee=profile.user).aggregate(Avg('rating'))['rating__avg']
    if avg_rating is not None:
        # Scale 1-5 to 0-100: (rating - 1) * 25
        metric.audience_score = int((avg_rating - 1) * 25)
    else:
        metric.audience_score = 0
    
    metric.save()

@receiver([post_save, post_delete], sender=Project)
def update_projects_score(sender, instance, **kwargs):
    if instance.profile:
        recalculate_metrics(instance.profile)

@receiver([post_save, post_delete], sender=Achievement)
def update_achievements_score(sender, instance, **kwargs):
    if instance.profile:
        recalculate_metrics(instance.profile)

@receiver([post_save, post_delete], sender=Media)
def update_media_score(sender, instance, **kwargs):
    if instance.profile:
        recalculate_metrics(instance.profile)

@receiver(post_save, sender=Profile)
def create_metric_for_new_profile(sender, instance, created, **kwargs):
    if created:
        ScoreMetric.objects.get_or_create(profile=instance)

@receiver([post_save, post_delete], sender=Review)
def update_audience_score(sender, instance, **kwargs):
    try:
        profile = Profile.objects.get(user=instance.reviewee)
        recalculate_metrics(profile)
    except Profile.DoesNotExist:
        pass
