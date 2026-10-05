from django.urls import path
from . import views

urlpatterns = [
    path('<int:profile_id>/claim/', views.claim_profile, name='claim_profile'),
]
