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


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'membership_type', 'created_at', 'created_by')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        # Set 'created_by' to the currently logged-in user when adding a new member
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

