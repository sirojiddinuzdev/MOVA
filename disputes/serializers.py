from rest_framework import serializers
from .models import Dispute, DisputeEvidence

class DisputeEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisputeEvidence
        fields = '__all__'
        read_only_fields = ('submitted_by', 'dispute')

class DisputeSerializer(serializers.ModelSerializer):
    evidence_timeline = DisputeEvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Dispute
        fields = '__all__'
        read_only_fields = ('opened_by', 'status')
