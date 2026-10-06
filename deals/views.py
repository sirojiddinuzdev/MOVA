from rest_framework import viewsets, permissions
from .models import Deal
from .serializers import DealSerializer

class IsParticipantOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client == request.user or obj.freelancer == request.user

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False):
            return Deal.objects.none()
        return Deal.objects.filter(client=user) | Deal.objects.filter(freelancer=user)
