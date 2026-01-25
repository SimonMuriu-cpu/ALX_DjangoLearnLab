# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from django.utils.html import escape
from django.core.exceptions import ValidationError, PermissionDenied
import re
from .models import Book, Library, CustomUser
from .forms import BookForm
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

# Security: Safe search function with input validation
def sanitize_search_input(search_term):
    """
    Sanitize and validate search input to prevent injection attacks.
    
    Args:
        search_term: User input for search
        
    Returns:
        Sanitized search term or None if invalid
    """
    if not search_term:
        return None
    
    # Remove potentially dangerous characters
    # Allow alphanumeric, spaces, hyphens, apostrophes, and basic punctuation
    sanitized = re.sub(r'[^\w\s\-\'",.!?]', '', search_term)
    
    # Limit length to prevent DoS
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    return sanitized.strip()

# Secure book list view with safe filtering
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect  # Additional CSRF protection
def book_list(request):
    """
    Secure view to list books with safe filtering.
    Uses Django's ORM to prevent SQL injection.
    """
    books = Book.objects.all()
    
    # Safe filtering using Django ORM (prevents SQL injection)
    author_filter = request.GET.get('author')
    library_filter = request.GET.get('library')
    
    if author_filter:
        # Use Q objects for safe query construction
        # The |escape ensures safe handling of user input
        books = books.filter(author__icontains=escape(author_filter))
    
    if library_filter and library_filter.isdigit():
        # Validate that library_filter is a number before using
        books = books.filter(library_id=int(library_filter))
    
    # Apply ordering safely
    sort_by = request.GET.get('sort', 'title')
    valid_sort_fields = ['title', 'author', 'published_date', '-title', '-author', '-published_date']
    if sort_by in valid_sort_fields:
        books = books.order_by(sort_by)
    
    context = {
        'books': books,
        'libraries': Library.objects.all(),
    }
    return render(request, 'bookshelf/book_list.html', context)

# Secure search view
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])  # Only allow safe methods
def book_search(request):
    """
    Secure search functionality with input validation.
    """
    if request.method == 'POST':
        # CSRF token is automatically checked by @csrf_protect
        
        search_term = request.POST.get('q', '')
        sanitized_term = sanitize_search_input(search_term)
        
        if not sanitized_term or len(sanitized_term) < 2:
            # Return to list with error message
            return render(request, 'bookshelf/book_list.html', {
                'books': Book.objects.all(),
                'error': 'Please enter at least 2 characters for search'
            })
        
        # SAFE: Using Django ORM with parameterized queries
        books = Book.objects.filter(
            Q(title__icontains=sanitized_term) | 
            Q(author__icontains=sanitized_term)
        )
        
        return render(request, 'bookshelf/book_list.html', {
            'books': books,
            'search_term': sanitized_term,
        })
    
    # GET request - show search form
    return render(request, 'bookshelf/search.html')

# Secure API endpoint with validation
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
@require_http_methods(["POST"])
def book_api_search(request):
    """
    Secure API endpoint for AJAX search.
    Validates all inputs and returns JSON safely.
    """
    try:
        search_term = request.POST.get('q', '')
        sanitized_term = sanitize_search_input(search_term)
        
        if not sanitized_term:
            return JsonResponse({'error': 'Invalid search term'}, status=400)
        
        # Safe ORM query
        books = Book.objects.filter(
            Q(title__icontains=sanitized_term) | 
            Q(author__icontains=sanitized_term)
        )[:10]  # Limit results to prevent DoS
        
        # Safe serialization
        book_data = []
        for book in books:
            book_data.append({
                'id': book.id,
                'title': escape(book.title),  # Escape for JSON
                'author': escape(book.author),
                'isbn': book.isbn,
            })
        
        return JsonResponse({'books': book_data})
    
    except Exception as e:
        # Log the error but don't expose details to user
        import logging
        logger = logging.getLogger('django.security')
        logger.error(f'API search error: {str(e)}')
        
        return JsonResponse({'error': 'Search failed'}, status=500)

# Secure create view with additional validation
class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_create'
    
    def handle_no_permission(self):
        # Log unauthorized access attempt
        import logging
        logger = logging.getLogger('django.security')
        logger.warning(f'Unauthorized create attempt by user: {self.request.user}')
        raise PermissionDenied("You don't have permission to create books.")
    
    def form_valid(self, form):
        """Additional security validation before saving."""
        try:
            # Validate ISBN format
            isbn = form.cleaned_data.get('isbn', '')
            if not re.match(r'^\d{10,13}$', isbn):
                form.add_error('isbn', 'ISBN must be 10-13 digits')
                return self.form_invalid(form)
            
            # Check for duplicate ISBN
            if Book.objects.filter(isbn=isbn).exists():
                form.add_error('isbn', 'A book with this ISBN already exists')
                return self.form_invalid(form)
            
            # All validation passed
            return super().form_valid(form)
            
        except Exception as e:
            # Log validation error
            import logging
            logger = logging.getLogger('django.security')
            logger.error(f'Book creation validation error: {str(e)}')
            form.add_error(None, 'An error occurred during validation')
            return self.form_invalid(form)

# Secure form template
def secure_form_example(request):
    """
    Example view demonstrating secure form handling.
    """
    if request.method == 'POST':
        # Django automatically checks CSRF token
        
        # Manual validation example
        user_input = request.POST.get('user_input', '')
        
        # 1. Validate length
        if len(user_input) > 1000:
            return HttpResponseBadRequest("Input too long")
        
        # 2. Sanitize HTML
        from django.utils.html import strip_tags
        sanitized_input = strip_tags(user_input)
        
        # 3. Escape for database
        from django.utils.html import escape
        safe_input = escape(sanitized_input)
        
        # 4. Use in safe context
        return render(request, 'bookshelf/secure_result.html', {
            'input': safe_input,
            'original': user_input[:100]  # Truncated for display
        })
    
    return render(request, 'bookshelf/form_example.html')