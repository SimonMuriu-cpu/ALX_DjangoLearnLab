from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/search/', views.book_search, name='book_search'),
    path('books/api/search/', views.book_api_search, name='book_api_search'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('secure-form/', views.secure_form_example, name='secure_form'),
    path('example-form/', views.example_form_view, name='example_form'),
    path('example-form/success/', views.example_form_success, name='example_form_success'),
    path('secure-search/', views.secure_search_demo, name='secure_search_demo'),
]