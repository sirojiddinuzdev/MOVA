from django.urls import path, include
from rest_framework_nested import routers
from .views import DisputeViewSet, DisputeEvidenceViewSet

router = routers.SimpleRouter()
router.register(r'', DisputeViewSet, basename='dispute')

dispute_router = routers.NestedSimpleRouter(router, r'', lookup='dispute')
dispute_router.register(r'evidence', DisputeEvidenceViewSet, basename='dispute-evidence')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(dispute_router.urls)),
]
