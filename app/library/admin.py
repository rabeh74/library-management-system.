from django.contrib import admin
from .models import Author, Book, Category, Member, Borrow, Review

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['member', 'book', 'borrow_date', 'return_date', 'returned']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'rating', 'created_at']

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Member)
