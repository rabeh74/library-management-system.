from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book , Category , Author , Member , Borrow , Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date', 'profile_picture']

class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many = True , required = False)
    author = AuthorSerializer(required = False)
    class Meta:
        model = Book
        fields = ['id','title', 'description', 'categories', 'author', 'cover', 'published_date']
    
    def create(self, validated_data):
        categories = validated_data.pop('categories' , [])
        author_data = validated_data.pop('author' , None)

        if author_data:
            author , created = Author.objects.get_or_create(**author_data)
            validated_data['author'] = author

        book = Book.objects.create(**validated_data)
        
        for category in categories:
            obj , created = Category.objects.get_or_create(**category)
            book.categories.add(obj)
        book.save()
        return book
    
    def update(self, instance, validated_data):
        categories = validated_data.pop('categories' , [])
        author_data = validated_data.pop('author' , None)
        for key , value in validated_data.items():
            setattr(instance , key , value)
        
        if categories:
            instance.categories.clear()
            for category in categories:
                category_obj , created = Category.objects.get_or_create(**category)
                instance.categories.add(category_obj)
        if author_data:
            author_obj , created = Author.objects.get_or_create(**author_data)
            instance.author = author_obj
        
        instance.save()
        return instance
    

    

    
    