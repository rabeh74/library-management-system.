import django_filters
from .models import Book , Category , Author , Member , Borrow , MEMBERSHIP_TYPE_CHOICES

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(method='filter_by_author_name')
    published_date = django_filters.DateFilter()
    published_date__gt = django_filters.DateFilter(field_name='published_date', lookup_expr='gt')
    published_date__lt = django_filters.DateFilter(field_name='published_date', lookup_expr='lt')
    categories = django_filters.CharFilter(method='filter_by_category_name')

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'categories' , 'published_date__gt' , 'published_date__lt']
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by('title')
    
    def filter_by_author_name(self, queryset, name, value):
        return queryset.filter(author__name__icontains=value) 
    
    def filter_by_category_name(self, queryset, name, value):
        return queryset.filter(categories__name=value).distinct()
    
class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Category
        fields = ['name']
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by('name')  

class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Author
        fields = ['name']
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by('name')  



  
class MemberFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    membership_type = django_filters.ChoiceFilter(choices=MEMBERSHIP_TYPE_CHOICES)
    address = django_filters.CharFilter(lookup_expr='icontains')
    borrows_book = django_filters.CharFilter(method='filter_by_borrows_book')
    
    class Meta:
        model = Member
        fields = ['name' , 'membership_type' , 'address' , 'borrows_book']
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by('name')
    
    def filter_by_borrows_book(self, queryset, name, value):
        return queryset.filter(borrows__book__title__icontains=value).distinct()

class BorrowFilter(django_filters.FilterSet):
    member = django_filters.CharFilter(method='filter_by_member_name')
    book = django_filters.CharFilter(method='filter_by_book_title')
    borrow_date = django_filters.DateFilter()
    return_date = django_filters.DateFilter()
    returned = django_filters.BooleanFilter()
    
    class Meta:
        model = Borrow
        fields = ['member' , 'book' , 'borrow_date' , 'return_date' , 'returned']
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by('borrow_date')
    
    def filter_by_member_name(self, queryset, name, value):
        return queryset.filter(member__name__icontains=value)
    
    def filter_by_book_title(self, queryset, name, value):
        return queryset.filter(book__title__icontains=value)