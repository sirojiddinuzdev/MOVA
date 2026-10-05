from django.contrib import admin
from .models import ScoreMetric

@admin.register(ScoreMetric)
class ScoreMetricAdmin(admin.ModelAdmin):
    list_display = ('profile', 'calculate_total_score')
