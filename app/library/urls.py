from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, CategoryViewSet , MemberViewSet , BorrowViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'members', MemberViewSet)
router.register(r'borrows', BorrowViewSet)

app_name = 'library'
urlpatterns = [
    path('', include(router.urls)),
]