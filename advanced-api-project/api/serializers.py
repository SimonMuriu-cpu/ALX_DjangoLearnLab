from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model with custom validation."""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """Custom validation to ensure publication year is not in the future."""
        current_year = timezone.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Optional: Add validation for reasonable past years
        # Books published before 1000 AD might be questionable
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year should be after 1000 AD."
            )
        
        return value
    
    def validate(self, data):
        """Optional: Add additional cross-field validation."""
        # Example: Check if title is not empty
        if 'title' in data and not data['title'].strip():
            raise serializers.ValidationError({
                'title': 'Title cannot be empty.'
            })
        
        return data

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model with nested books."""
    
    # Using BookSerializer as a nested serializer for related books
    # Note: books is the related_name we set in the Book model's ForeignKey
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id', 'books']
    
    def validate_name(self, value):
        """Custom validation for author name."""
        if not value.strip():
            raise serializers.ValidationError("Author name cannot be empty.")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Author name must be at least 2 characters long.")
        
        return value.strip()