from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .serializers import UserActivitySerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Location
from .serializers import LocationSummarySerializer


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_user_activity(request):
    serializer = UserActivitySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user_activity = serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationSummaryList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSummarySerializer
    permission_classes = [IsAuthenticated]