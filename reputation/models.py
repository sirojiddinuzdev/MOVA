from django.db import models
from profiles.models import Profile

class ScoreMetric(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='score_metrics')
    audience_score = models.IntegerField(default=0, help_text="0-100")
    engagement_score = models.IntegerField(default=0, help_text="0-100")
    media_presence_score = models.IntegerField(default=0, help_text="0-100")
    achievements_score = models.IntegerField(default=0, help_text="0-100")
    projects_score = models.IntegerField(default=0, help_text="0-100")
    activity_score = models.IntegerField(default=0, help_text="0-100")
    impact_score = models.IntegerField(default=0, help_text="0-100")

    def calculate_total_score(self):
        # A simple average for demonstration. Can be weighted in the future.
        total = (self.audience_score + self.engagement_score + 
                 self.media_presence_score + self.achievements_score + 
                 self.projects_score + self.activity_score + self.impact_score)
        return total // 7

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically update the profile's recognition score
        self.profile.recognition_score = self.calculate_total_score()
        self.profile.save()

    def __str__(self):
        return f"Metrics for {self.profile.full_name}"
