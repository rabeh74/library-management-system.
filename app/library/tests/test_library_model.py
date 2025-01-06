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
        user = create_user(**user_params)
        member = Member.objects.create(
            name='test member',
            phone='1234567890',
            address='test address',
            membership_type='premium',
            created_by=user
        )

        self.assertEqual(member.name, "test member")
        self.assertEqual(member.phone, "1234567890")
        self.assertEqual(member.address, "test address")
        self.assertEqual(member.membership_type, "premium")
        self.assertEqual(member.created_by, user)
        self.assertEqual(str(member), "test member")
        

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
        member = Member.objects.create(name='test member', phone='1234567890', address='test address', membership_type='premium')
        author, category = self.create_author_and_category()
        book = self.create_book(author, category)

        borrow = Borrow.objects.create(
            member=member, book=book, borrow_date=datetime.date(2024, 12, 1)
        )

        self.assertEqual(borrow.member, member)
        self.assertEqual(borrow.book, book)
        self.assertEqual(borrow.borrow_date, datetime.date(2024, 12, 1))
        self.assertFalse(borrow.returned)