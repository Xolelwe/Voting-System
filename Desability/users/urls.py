from django.urls import path
from .views import RegisterUserView, UserListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('all/', UserListView.as_view(), name='user-list'),
]

from .views import UserProfileView

urlpatterns += [
    path('profile/', UserProfileView.as_view(), name='profile'),
]
