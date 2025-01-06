from django.db import models
import uuid
from user.models import CustomUser
import datetime
from django.utils.timezone import now

from django.db import models
from django.conf import settings


def upload_to_authors(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        return 'authors/{}/{}'.format(instance.name, filename)
        
def upload_to_books(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        return 'books/{}/{}'.format(instance.title, filename)

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    profile_picture = models.ImageField(upload_to=upload_to_authors, blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE , related_name='books' , null=True , blank=True)  
    categories = models.ManyToManyField(Category)
    cover = models.ImageField(upload_to=upload_to_books, blank=True, null=True)

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=255 , default='Anonymous')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    membership_type = models.CharField(
        max_length=50,
        choices=[('regular', 'Regular'), ('premium', 'Premium')],
        default='regular'
    )
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_members',
    )

    def __str__(self):
        return self.name


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateField(default=datetime.date.today)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.user.email} borrowed {self.book.title}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    rating = models.PositiveIntegerField()  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.book.title} by {self.member.user.email}"
