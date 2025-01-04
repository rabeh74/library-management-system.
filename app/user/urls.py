from django.urls import path
from .views import UserCreateView, UserRetrieveUpdateView , CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('update/<int:id>/', UserRetrieveUpdateView.as_view(), name='update_user'),
]