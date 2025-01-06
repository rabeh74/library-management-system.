from django.shortcuts import render



# Create your views here.
from .serializers import BookSerializer , CategorySerializer , AuthorSerializer , MemberSerializer , BorrowSerializer
from rest_framework import viewsets , permissions , authentication
from .models import Book , Category , Author , Member , Borrow , Review
from rest_framework.viewsets import ModelViewSet
from .filters import BookFilter , CategoryFilter , AuthorFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='author',
                description='Filter books by author',
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name='category',
                description='Filter books by category',
                required=False,
                type=OpenApiTypes.INT,
            ),
        ],
        responses={200: BookSerializer(many=True)},
    ),
    retrieve=extend_schema(
        responses={200: BookSerializer},
    ),
    create=extend_schema(
        request=BookSerializer,
        responses={201: BookSerializer},
    ),
    update=extend_schema(
        request=BookSerializer,
        responses={200: BookSerializer},
    ),
    partial_update=extend_schema(
        request=BookSerializer,
        responses={200: BookSerializer},
    ),
    destroy=extend_schema(
        responses={204: None},
    ),
)

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

class BorrowViewSet(ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

