# bookshelf/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, Library

class Command(BaseCommand):
    help = 'Creates default groups with permissions'
    
    def handle(self, *args, **kwargs):
        # Get content types
        book_content_type = ContentType.objects.get_for_model(Book)
        library_content_type = ContentType.objects.get_for_model(Library)
        
        # Get permissions
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        library_permissions = Permission.objects.filter(content_type=library_content_type)
        
        # Create Viewers group (can_view only)
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.clear()
        can_view_book = Permission.objects.get(codename='can_view', content_type=book_content_type)
        can_view_library = Permission.objects.get(codename='can_view', content_type=library_content_type)
        viewers_group.permissions.add(can_view_book, can_view_library)
        self.stdout.write(self.style.SUCCESS('Created/Updated Viewers group'))
        
        # Create Editors group (can_view, can_create, can_edit)
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.clear()
        for perm in book_permissions.filter(codename__in=['can_view', 'can_create', 'can_edit']):
            editors_group.permissions.add(perm)
        for perm in library_permissions.filter(codename__in=['can_view', 'can_create', 'can_edit']):
            editors_group.permissions.add(perm)
        self.stdout.write(self.style.SUCCESS('Created/Updated Editors group'))
        
        # Create Admins group (all permissions)
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.clear()
        for perm in book_permissions:
            admins_group.permissions.add(perm)
        for perm in library_permissions:
            admins_group.permissions.add(perm)
        self.stdout.write(self.style.SUCCESS('Created/Updated Admins group'))