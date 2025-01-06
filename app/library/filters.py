import django_filters
from .models import Book , Category , Author

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(method='filter_by_author_name')
    published_date = django_filters.DateFilter()
    categories = django_filters.CharFilter(method='filter_by_category_name')

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'categories']
    
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

  
