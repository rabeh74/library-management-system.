from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, CategoryViewSet , MemberViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'members', MemberViewSet)
app_name = 'library'
urlpatterns = [
    path('', include(router.urls)),
]