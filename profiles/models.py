from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile', help_text="Linked user account if claimed")
    full_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(blank=True, null=True, help_text="When they started their career")
    current_activity = models.CharField(max_length=255, blank=True, help_text="What they are currently doing")
    
    # Verification
    is_identity_verified = models.BooleanField(default=False, help_text="Is this profile managed by the real person?")
    is_public_figure = models.BooleanField(default=False, help_text="Is this person recognized by MOVA as a public figure?")
    is_claimed = models.BooleanField(default=False, help_text="Has the person claimed this profile?")
    
    # Mova Score
    recognition_score = models.IntegerField(default=0, help_text="0-100 MOVA Recognition Score")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class SocialLink(models.Model):
    PLATFORM_CHOICES = (
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('telegram', 'Telegram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('other', 'Other'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.profile.full_name} - {self.platform}"

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.profile.full_name})"

class Achievement(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.profile.full_name})"

class CareerTimeline(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='career_timeline')
    year_or_date = models.CharField(max_length=50, help_text="e.g., '2020' or 'Mar 2020'")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['year_or_date']

    def __str__(self):
        return f"{self.year_or_date} - {self.title}"

class Media(models.Model):
    MEDIA_TYPES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    url = models.URLField()
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.media_type} for {self.profile.full_name}"
