from django import forms
from bookshelf.models import Book


Book = None
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
