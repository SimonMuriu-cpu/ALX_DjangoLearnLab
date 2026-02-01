from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsAdminOrReadOnly, IsBookOwner

# Create your views here.

# Viewsets for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Set permission classes based on action
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow anyone to view books
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # Only authenticated users can create books
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            # Only owners or admins can update books
            permission_classes = [IsAuthenticated, IsBookOwner | IsAdminUser]
        elif self.action == 'destroy':
            # Only admins can delete books
            permission_classes = [IsAdminUser]
        else:
            # Default to requiring authentication
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    # Filter queryset based on user permissions
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            # Admins can see all books
            return Book.objects.all()
        elif user.is_authenticated:
            # Authenticated users can see their own books + public books
            return Book.objects.filter(owner=user) | Book.objects.filter(owner__isnull=True)
        else:
            # Anonymous users can only see public books
            return Book.objects.filter(owner__isnull=True)
    
    # Auto-set owner when creating a book
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'author', 'published_date']
    ordering = ['-published_date']