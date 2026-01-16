from django.db import models

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
