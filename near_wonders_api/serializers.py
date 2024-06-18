from rest_framework import serializers
from .models import Location, Image, UserActivity
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Include the user data
        serializer = UserSerializer(self.user)
        data['user'] = serializer.data

        # Include token expiration times
        refresh = self.get_token(self.user)
        data['refresh_expiration'] = refresh.access_token.lifetime.total_seconds()
        data['access_expiration'] = refresh.lifetime.total_seconds()

        return data


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        if not username:
            raise serializers.ValidationError({'username': 'Email is required.'})
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})
        if not first_name:
            raise serializers.ValidationError({'first_name': 'First name is required.'})
        if not last_name:
            raise serializers.ValidationError({'last_name': 'Last name is required.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            email=username,
            first_name=first_name,
            last_name=last_name
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')
    user_since = serializers.DateTimeField(source='date_joined')

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'user_since']


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class LocationField(serializers.Field):
    def to_internal_value(self, data):
        if 'id' in data:
            try:
                location = Location.objects.get(id=data['id'])
                return location
            except Location.DoesNotExist:
                raise serializers.ValidationError('Location with this ID does not exist.')
        else:
            required_fields = ['name', 'latitude', 'longitude', 'description', 'best_season', 'activities']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError({field: f'{field} is required.'})
            return data

    def to_representation(self, value):
        if isinstance(value, Location):
            return LocationSerializer(value).data
        return value


class UserActivitySerializer(serializers.ModelSerializer):
    location = LocationField()
    images = ImageSerializer(many=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'location', 'activities', 'user_notes', 'images']

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        images_data = validated_data.pop('images')

        user = self.context['request'].user

        if isinstance(location_data, Location):
            location = location_data
        else:
            location_name = location_data['name']
            activities = validated_data['activities']
            if not location_name:
                raise serializers.ValidationError({'location/name': 'Location name is required.'})
            if not activities:
                raise serializers.ValidationError({'activities': 'Activities are required.'})

            location, created = Location.objects.get_or_create(
                name=location_name,
                defaults={**location_data, 'created_by': user}
            )

        # Remove the user key from validated_data to avoid conflict
        user_activity_data = validated_data.copy()
        user_activity_data.pop('user', None)

        # Create the user activity
        user_activity = UserActivity.objects.create(location=location, user=user, **user_activity_data)

        # Create and add images to the user activity
        for image_data in images_data:
            image = Image.objects.create(location=location, uploaded_by=user, **image_data)
            user_activity.images.add(image)

        return user_activity


class LocationSummarySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    date = serializers.DateTimeField(source='created_at')
    images = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()
    bookmarks = serializers.IntegerField(default=0)  # Assuming you want to count bookmarks, adapt as needed

    class Meta:
        model = Location
        fields = ['id', 'title', 'date', 'images', 'bookmarks', 'activities', 'latitude', 'longitude']

    def get_images(self, obj):
        return [image.image.url for image in obj.preview_images]

    def get_activities(self, obj):
        return obj.activities.split(',')  # Assuming activities are stored as a comma-separated string
