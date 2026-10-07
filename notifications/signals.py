from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from disputes.models import Dispute
from profiles.models import ProfileClaimRequest
from deals.models import Deal
from notifications.models import Notification

@receiver(post_save, sender=Dispute)
def notify_dispute_opened(sender, instance, created, **kwargs):
    if created:
        deal = instance.deal
        opened_by = instance.opened_by
        other_party = deal.client if opened_by == deal.freelancer else deal.freelancer
        
        Notification.objects.create(
            user=other_party,
            title="A dispute has been opened",
            message=f"A dispute has been opened by {opened_by.username} for Deal #{deal.id}."
        )

@receiver(pre_save, sender=ProfileClaimRequest)
def notify_claim_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = ProfileClaimRequest.objects.get(pk=instance.pk)
        if old_instance.status != instance.status and instance.status in ['approved', 'rejected']:
            Notification.objects.create(
                user=instance.requester,
                title=f"Profile Claim {instance.status.capitalize()}",
                message=f"Your claim request for profile '{instance.profile.full_name}' has been {instance.status}."
            )

@receiver(pre_save, sender=Deal)
def notify_deal_completed(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Deal.objects.get(pk=instance.pk)
        if old_instance.status != instance.status and instance.status == 'completed':
            # Notify both
            Notification.objects.create(
                user=instance.client,
                title="Deal Completed",
                message=f"Deal #{instance.id} with {instance.freelancer.username} is now completed."
            )
            Notification.objects.create(
                user=instance.freelancer,
                title="Deal Completed",
                message=f"Deal #{instance.id} with {instance.client.username} is now completed."
            )
