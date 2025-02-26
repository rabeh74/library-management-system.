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
        fields = ['id','title', 'description', 'categories', 'author', 'cover', 'published_date' , 'available_copies']
    

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
    

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','name', 'phone', 'address', 'membership_type', 'created_at', 'created_by']
    


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return Member.objects.create(**validated_data)

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id','member', 'book', 'borrow_date', 'return_date', 'returned']
    
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)
        

    def create(self, validated_data):
        book = validated_data['book']
        if book.available_copies == 0:
            raise serializers.ValidationError('No available copies of this book')
        book.available_copies -= 1
        book.save()
        return Borrow.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        book = instance.book
        returned = validated_data.get('returned' , False)
        if returned:
            book.available_copies += 1
            book.save()
        for key , value in validated_data.items():
            setattr(instance , key , value)
        
        instance.save()
        return instance
    
