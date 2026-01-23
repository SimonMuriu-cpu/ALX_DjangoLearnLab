from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic.detail import DetailView, CreateView, UpdateView, DeleteView, ListView

from bookshelf.models import Book, Library
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy


# from .forms import BookForm


Book = None
Library = None
BookForm = None
# Create your views here.
def list_books(request):
  books = Book.objects.all()
  return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
  mode =Library
  template_name = 'relationship_app/library_detail.html'
  context_object_name = 'library'

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # logs user in immediately
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# Add Book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # update as needed
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# Edit Book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# Delete Book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})


# Enforcing permissions in class-based views
# View to list books - requires can_view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for library detail - requires can_view permission
class LibraryDetailView(PermissionRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    permission_required = 'bookshelf.can_view'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to view libraries.")

# Create view for books - requires can_create permission
class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('list_books')
    permission_required = 'bookshelf.can_create'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to create books.")

# Update view for books - requires can_edit permission
class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('list_books')
    permission_required = 'bookshelf.can_edit'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to edit books.")

# Delete view for books - requires can_delete permission
class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'relationship_app/book_confirm_delete.html'
    success_url = reverse_lazy('list_books')
    permission_required = 'bookshelf.can_delete'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to delete books.")

# Library list view - requires can_view permission
class LibraryListView(PermissionRequiredMixin, ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    permission_required = 'bookshelf.can_view'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to view libraries.")