from django.shortcuts import render, get_object_or_404

from django.views.generic.detail import DetailView

from .models import Library
from .models import Book

# Create your views here.
def list_books(request):
  books = Book.objects.all()
  return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
  mode =Library
  template_name = 'relationship_app/library_detail.html'
  context_object_name = 'library'

  