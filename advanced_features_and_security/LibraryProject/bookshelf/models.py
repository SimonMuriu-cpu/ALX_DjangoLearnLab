from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Custom User Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, date_of_birth, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        if not date_of_birth:
            raise ValueError(_('The Date of Birth must be set'))
            
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            date_of_birth=date_of_birth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, date_of_birth, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, username, date_of_birth, password, **extra_fields)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'))
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        verbose_name=_('Profile Photo'),
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return self.email

# Library and Book models

# Updating the Library model to include permissions:

class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    librarian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = [
            ("can_view", "Can view library"),
            ("can_create", "Can create library"),
            ("can_edit", "Can edit library"),
            ("can_delete", "Can delete library"),
        ]
    
    def __str__(self):
        return self.name

# Updating the Book model to include permissions:

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name='books'
    )
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
    
    def __str__(self):
        return self.title

# Models for relationship_app (moved here to avoid duplicates)
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"