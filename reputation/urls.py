from rest_framework.routers import DefaultRouter
from .views import ScoreMetricViewSet

router = DefaultRouter()
router.register(r'', ScoreMetricViewSet, basename='scoremetric')

urlpatterns = router.urls
