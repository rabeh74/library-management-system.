from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
from django.contrib.auth import get_user_model
from decimal import Decimal

from library.models import Author, Book, Category, Borrow, Review, Member
from django.core.files.uploadedfile import SimpleUploadedFile


def create_user(**params):
    return get_user_model().objects.create_user(**params)

user_params = {
    'email':'test@email.com',
    'password':'testpass',
    'full_name':'Test User',
    'phone_number':'1234567890',
}



class LibraryModelsTest(TestCase):
    
    def create_user_and_member(self):
        user = create_user(**user_params)
        member = Member.objects.create(user=user, membership_expiry=datetime.date(2025, 1, 1))
        return user, member

    def create_author_and_category(self):
        author = Author.objects.create(name="J.K. Rowling")
        category = Category.objects.create(name="Fantasy")
        return author, category

    def create_book(self, author, category):
        book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            description="A magical adventure",
            published_date=datetime.date(1997, 6, 26),
            author=author,
        )
        book.categories.add(category)
        return book

    def test_member_creation(self):
        user, member = self.create_user_and_member()
        self.assertEqual(member.user, user)
        self.assertEqual(member.membership_expiry, datetime.date(2025, 1, 1))
        self.assertEqual(str(member), user.full_name)

    def test_author_and_category_creation(self):
        author, category = self.create_author_and_category()
        self.assertEqual(author.name, "J.K. Rowling")
        self.assertEqual(str(author), "J.K. Rowling")
        self.assertEqual(category.name, "Fantasy")
        self.assertEqual(str(category), "Fantasy")

    def test_book_creation(self):
        author, category = self.create_author_and_category()
        book = self.create_book(author, category)

        self.assertEqual(book.title, "Harry Potter and the Philosopher's Stone")
        self.assertEqual(book.description, "A magical adventure")
        self.assertEqual(book.published_date, datetime.date(1997, 6, 26))
        self.assertEqual(book.author, author)
        self.assertIn(category, book.categories.all())
        self.assertEqual(book.categories.count(), 1)

    def test_borrow_creation(self):
        user, member = self.create_user_and_member()
        author, category = self.create_author_and_category()
        book = self.create_book(author, category)

        borrow = Borrow.objects.create(
            member=member, book=book, borrow_date=datetime.date(2024, 12, 1)
        )

        self.assertEqual(borrow.member, member)
        self.assertEqual(borrow.book, book)
        self.assertEqual(borrow.borrow_date, datetime.date(2024, 12, 1))
        self.assertFalse(borrow.returned)

    def test_review_creation(self):
        user, member = self.create_user_and_member()
        author, category = self.create_author_and_category()
        book = self.create_book(author, category)

        review = Review.objects.create(
            book=book, member=member, review_text="Amazing book!", rating=5
        )

        self.assertEqual(review.book, book)
        self.assertEqual(review.member, member)
        self.assertEqual(review.review_text, "Amazing book!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(str(review), f"Review for {book.title} by {member.user.email}")
