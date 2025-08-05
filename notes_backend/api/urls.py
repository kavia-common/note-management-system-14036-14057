from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    RegisterView,
    LoginView,
    LogoutView,
    UserInfoView,
    NoteViewSet
)

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', UserInfoView.as_view(), name='user_info'),
    path('', include(router.urls)),
]
