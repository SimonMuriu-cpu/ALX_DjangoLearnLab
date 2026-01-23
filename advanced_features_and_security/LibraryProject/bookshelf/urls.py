# bookshelf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('libraries/', views.library_list, name='library_list'),
    path('books/manage/', views.book_management, name='book_management'),
    path('books/create-manual/', views.create_book_manual, name='create_book_manual'),
]