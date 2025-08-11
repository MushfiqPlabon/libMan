from rest_framework import serializers
from .models import Author, Member, Book, BorrowRecord

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, source='author')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'isbn', 'category', 'availability_status']

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'