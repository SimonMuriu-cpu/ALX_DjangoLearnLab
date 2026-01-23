from django.shortcuts import render

# Create your views here.
# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Book, Library, CustomUser
from .forms import BookForm  # You'll need to create this

# Function-based view with permission_required decorator
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books. Requires 'can_view' permission.
    Uses @permission_required decorator with raise_exception=True.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Class-based view for creating books
class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_create'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to create books.")

# Class-based view for updating books
class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_edit'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to edit books.")

# Class-based view for deleting books  
class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_delete'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to delete books.")

# View for library list
@permission_required('bookshelf.can_view', raise_exception=True)
def library_list(request):
    """
    View to list all libraries. Requires 'can_view' permission.
    Uses @permission_required decorator with raise_exception=True.
    """
    libraries = Library.objects.all()
    return render(request, 'bookshelf/library_list.html', {'libraries': libraries})

# View to demonstrate multiple permissions
@permission_required(['bookshelf.can_view', 'bookshelf.can_edit'], raise_exception=True)
def book_management(request):
    """
    View that requires multiple permissions.
    Demonstrates checking for both 'can_view' and 'can_edit' permissions.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_management.html', {'books': books})

# View with login requirement and permission check
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book_manual(request):
    """
    View that combines @login_required and @permission_required.
    Demonstrates chaining decorators.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/create_book_manual.html', {'form': form})