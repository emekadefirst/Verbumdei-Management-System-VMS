from student.models import Student
from rest_framework import serializers
from .models import Book, Loan, Shelf, BookCategory


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ["id", "name"]
        read_only_fields = ['id']


class LoanSerializer(serializers.ModelSerializer):
    book =serializers.SlugRelatedField(slug_field="id", queryset=Book.objects.all())
    student = serializers.SlugRelatedField(slug_field="registration_id", queryset=Student.objects.all())
    class Meta:
        model = Loan
        fields = ["id", "student", "book", "action", "borrowed_at", "return_date", "actual_return_date"]
        read_only_fields = ["id", "borrowed_at"]

    def create(self, validated_data):
        loan = Loan.objects.create(**validated_data)
        return loan

    def update(self, instance, validated_data):
        instance.student = validated_data.get("student", instance.student)
        instance.book = validated_data.get("book", instance.book)
        instance.action = validated_data.get("action", instance.action)
        instance.borrowed_at = validated_data.get("borrowed_at", instance.borrowed_at)
        instance.return_date = validated_data.get("return_date", instance.return_date)
        instance.actual_return_date = validated_data.get("actual_return_date", instance.actual_return_date)
        instance.save()
        return instance


class CreateBookSerializer(serializers.ModelSerializer):
    category =serializers.SlugRelatedField(slug_field="name", queryset=BookCategory.objects.all())
    shelf =serializers.SlugRelatedField(slug_field="name", queryset=Shelf.objects.all())
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'copies', 'category', 'shelf', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.author = validated_data.get("author", instance.author)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        instance.copies = validated_data.get("copies", instance.copies)
        instance.category = validated_data.get("category", instance.category)
        instance.shelf = validated_data.get("shelf", instance.shelf)
        instance.save()
        return instance

class GetLoanListSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class BookListSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class CategoryListSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['id', 'code', 'loaction', 'section', 'description']
        read_only_fields = ['id', 'code']

    def create(self, validated_data):
        book = Shelf.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        instance.code = validated_data.get("code", instance.code)
        instance.location = validated_data.get("location", instance.location)
        instance.section = validated_data.get("section", instance.section)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
