from django.urls import path
from .auth_views import UserRegistrationView, UserDeleteView
from .views import create_user_activity, LocationSummaryList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-user/', UserDeleteView.as_view(), name='delete_user'),
    path('user-activity/', create_user_activity, name='create_user_activity'),
    path('locations/', LocationSummaryList.as_view(), name='location_summary_list'),
]
