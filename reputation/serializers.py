from rest_framework import serializers
from .models import ScoreMetric

class ScoreMetricSerializer(serializers.ModelSerializer):
    total_score = serializers.IntegerField(source='calculate_total_score', read_only=True)

    class Meta:
        model = ScoreMetric
        fields = '__all__'
        read_only_fields = ('profile', 'audience_score', 'endorsement_score', 'activity_score', 'media_score')
