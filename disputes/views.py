from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Dispute, DisputeEvidence
from .serializers import DisputeSerializer, DisputeEvidenceSerializer

class IsParticipantOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only clients or freelancers of the deal can modify
        return obj.deal.client == request.user or obj.deal.freelancer == request.user

class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(opened_by=self.request.user)

class DisputeEvidenceViewSet(viewsets.ModelViewSet):
    queryset = DisputeEvidence.objects.all()
    serializer_class = DisputeEvidenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        dispute = get_object_or_404(Dispute, pk=self.kwargs.get('dispute_pk'))
        serializer.save(submitted_by=self.request.user, dispute=dispute)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return DisputeEvidence.objects.none()
        return DisputeEvidence.objects.filter(dispute_id=self.kwargs.get('dispute_pk'))
