from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from rest_framework.authtoken.views import obtain_auth_token

from .views_auth import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView


router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),  # DRF built-in
    path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Public API endpoints
    
    
    # Protected API endpoints (via router)
    path('', include(router.urls)),
    
]
