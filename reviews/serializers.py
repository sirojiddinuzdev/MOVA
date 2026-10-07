from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewer',)

    def validate(self, attrs):
        deal = attrs.get('deal')
        reviewee = attrs.get('reviewee')
        rating = attrs.get('rating')
        reviewer = self.context['request'].user

        if rating < 1 or rating > 5:
            raise serializers.ValidationError({"rating": "Rating must be between 1 and 5."})

        if deal.status != 'completed':
            raise serializers.ValidationError({"deal": "Reviews can only be created for completed deals."})

        if reviewer == deal.client:
            expected_reviewee = deal.freelancer
        elif reviewer == deal.freelancer:
            expected_reviewee = deal.client
        else:
            raise serializers.ValidationError("You must be a participant in this deal to leave a review.")

        if reviewee != expected_reviewee:
            raise serializers.ValidationError({"reviewee": f"Reviewee must be the other participant in the deal."})

        return attrs
