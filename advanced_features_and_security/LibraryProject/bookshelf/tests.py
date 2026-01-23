from django.test import TestCase

# Create your tests here.
# bookshelf/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import CustomUser, Book, Library

class PermissionTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            date_of_birth='2000-01-01',
            password='testpass123'
        )
        
        # Create test library
        self.library = Library.objects.create(
            name='Test Library',
            location='Test Location'
        )
        
        # Create test book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            library=self.library,
            published_date='2023-01-01'
        )
        
        # Get permissions
        book_content_type = ContentType.objects.get_for_model(Book)
        self.can_view = Permission.objects.get(codename='can_view', content_type=book_content_type)
        self.can_create = Permission.objects.get(codename='can_create', content_type=book_content_type)
        self.can_edit = Permission.objects.get(codename='can_edit', content_type=book_content_type)
        self.can_delete = Permission.objects.get(codename='can_delete', content_type=book_content_type)
        
        self.client = Client()
    
    def test_viewer_permissions(self):
        """Test that viewer can view but not edit."""
        # Add only can_view permission
        self.user.user_permissions.add(self.can_view)
        self.client.login(email='test@example.com', password='testpass123')
        
        # Should be able to view
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Should NOT be able to edit
        response = self.client.get(reverse('book_edit', args=[self.book.id]))
        self.assertEqual(response.status_code, 403)
    
    def test_editor_permissions(self):
        """Test that editor can view and edit but not delete."""
        # Add can_view, can_create, can_edit permissions
        self.user.user_permissions.add(self.can_view, self.can_create, self.can_edit)
        self.client.login(email='test@example.com', password='testpass123')
        
        # Should be able to view
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Should be able to access edit page
        response = self.client.get(reverse('book_edit', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        
        # Should NOT be able to delete
        response = self.client.get(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(response.status_code, 403)
    
    def test_admin_permissions(self):
        """Test that admin can do everything."""
        # Add all permissions
        self.user.user_permissions.add(self.can_view, self.can_create, self.can_edit, self.can_delete)
        self.client.login(email='test@example.com', password='testpass123')
        
        # Should be able to do everything
        for url_name in ['book_list', 'book_create', 'book_edit', 'book_delete']:
            if url_name in ['book_edit', 'book_delete']:
                response = self.client.get(reverse(url_name, args=[self.book.id]))
            else:
                response = self.client.get(reverse(url_name))
            self.assertIn(response.status_code, [200, 302])  # 200 OK or 302 redirect
    
    def test_raise_exception_true(self):
        """Test that raise_exception=True returns 403 instead of redirect."""
        # User has no permissions
        self.client.login(email='test@example.com', password='testpass123')
        
        # Should get 403 Forbidden, not redirect to login
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 403)