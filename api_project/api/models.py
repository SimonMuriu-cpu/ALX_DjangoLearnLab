from django.db import models
from httpcore import request
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='books',
        null=True,  # Allow null for existing records
        blank=True
    )
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-set owner if not specified
        if not self.owner_id:
            from django.contrib.auth import get_user
            try:
                self.owner = get_user(self)
            except:
                pass
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['title']