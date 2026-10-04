from django.db import models
from django.conf import settings
from deals.models import Deal
from django.core.exceptions import ValidationError

class Review(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('deal', 'reviewer')

    def save(self, *args, **kwargs):
        if self.deal.status != 'completed':
            raise ValidationError("Reviews can only be created for completed deals.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.reviewer.username} for Deal {self.deal.id}"
