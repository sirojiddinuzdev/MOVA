from rest_framework import viewsets, mixins, permissions
from .models import ScoreMetric
from .serializers import ScoreMetricSerializer

class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.profile.user == request.user

class ScoreMetricViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = ScoreMetric.objects.all()
    serializer_class = ScoreMetricSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]
