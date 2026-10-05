from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Profile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim_profile(request, profile_id):
    """
    Mock endpoint to claim a profile.
    In a real app, this would require verification documents.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    
    if profile.is_claimed:
        return Response({"error": "Profile is already claimed"}, status=status.HTTP_400_BAD_REQUEST)
        
    # Link the current user to the profile
    profile.user = request.user
    profile.is_claimed = True
    # Verification process could be asynchronous in reality
    profile.is_identity_verified = True
    profile.save()
    
    return Response({"message": f"Successfully claimed profile: {profile.full_name}"}, status=status.HTTP_200_OK)
