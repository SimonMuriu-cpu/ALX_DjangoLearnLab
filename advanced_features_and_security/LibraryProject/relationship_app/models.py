from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.conf import settings



# Create your models here.

"""Model representing an author in the relationship app."""
class Author(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name
  

"""Model representing books written by authors."""
class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

  def __str__(self):
    return self.title
  
  class Meta:
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )
  

  """Library model representing librariies containing books.
  """
class Library(models.Model):
  name = models.CharField(max_length=100)
  books = models.ManyToManyField(Book, related_name='libraries')

  def __str__(self):
    return self.name
  
  """Librarian model representing librarians managing libraries."""
class Librarian(models.Model):
  name = models.CharField(max_length=100)
  library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
  def __str__(self):
    return self.name
  

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Member'
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    objects = CustomUserManager()

    class Meta:
        app_label = 'relationship_app'

    def __str__(self):
        return self.username
