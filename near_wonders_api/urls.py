from django.urls import path
from .views import TodoCreateView, TodoUpdateView, TodoDeleteView, TodoListView
from .auth_views import UserRegistrationView, UserDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view(), name='todo_create'),
    path('todo/update/<int:pk>/', TodoUpdateView.as_view(), name='todo_update'),
    path('todo/delete/<int:pk>/', TodoDeleteView.as_view(), name='todo_delete'),
    path('todo/', TodoListView.as_view(), name='todo_list'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-user/', UserDeleteView.as_view(), name='delete_user'),
]
