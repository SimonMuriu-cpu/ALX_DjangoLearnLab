from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

# Viewsets for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'author', 'published_date']
    ordering = ['-published_date']