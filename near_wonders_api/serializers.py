from rest_framework import serializers
from .models import Location, Image, UserActivity


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'description', 'activities', 'best_season', 'latitude', 'longitude']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class UserActivitySerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = UserActivity
        fields = ['location', 'activities', 'user_notes', 'images']

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        images_data = validated_data.pop('images')

        # Get the user from the context
        user = self.context['request'].user

        # Create or get the location
        location, created = Location.objects.get_or_create(
            name=location_data['name'],
            defaults={**location_data, 'created_by': user}
        )

        # Remove the user key from validated_data to avoid conflict
        validated_data.pop('user', None)

        # Create the user activity
        user_activity = UserActivity.objects.create(location=location, user=user, **validated_data)

        # Create and add images to the user activity
        for image_data in images_data:
            image = Image.objects.create(location=location, uploaded_by=user, **image_data)
            user_activity.images.add(image)

        return user_activity
