from django.contrib import admin
from .models import Dispute, DisputeEvidence

class DisputeEvidenceInline(admin.TabularInline):
    model = DisputeEvidence
    extra = 1

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('id', 'deal', 'opened_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [DisputeEvidenceInline]

@admin.register(DisputeEvidence)
class DisputeEvidenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'dispute', 'submitted_by', 'created_at')
