from rest_framework import serializers
from .models import Author, Member, Book, BorrowRecord

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, help_text="Unique identifier for the author.")
    name = serializers.CharField(max_length=200, help_text="The full name of the author.")
    biography = serializers.CharField(allow_null=True, required=False, help_text="A brief biography of the author.")

    class Meta:
        model = Author
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, help_text="Unique identifier for the member.")
    name = serializers.CharField(max_length=200, help_text="The full name of the member.")
    email = serializers.EmailField(max_length=254, help_text="The email address of the member.")
    membership_date = serializers.DateField(read_only=True, help_text="The date the member joined.")

    class Meta:
        model = Member
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True, help_text="The author of the book.")
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, source='author', help_text="The ID of the author.")
    id = serializers.IntegerField(read_only=True, help_text="Unique identifier for the book.")
    title = serializers.CharField(max_length=200, help_text="The title of the book.")
    isbn = serializers.CharField(max_length=13, help_text="The International Standard Book Number (ISBN) of the book.")
    category = serializers.CharField(max_length=100, help_text="The category or genre of the book.")
    availability_status = serializers.BooleanField(help_text="Indicates if the book is currently available for borrowing.")

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'isbn', 'category', 'availability_status']

class BorrowRecordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, help_text="Unique identifier for the borrow record.")
    borrow_date = serializers.DateField(read_only=True, help_text="The date the book was borrowed.")
    return_date = serializers.DateField(allow_null=True, required=False, help_text="The date the book was returned.")
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), help_text="The ID of the borrowed book.")
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), help_text="The ID of the member who borrowed the book.")

    class Meta:
        model = BorrowRecord
        fields = '__all__'

class BorrowBookInputSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(help_text="The ID of the book to borrow.")
    member_id = serializers.IntegerField(help_text="The ID of the member borrowing the book.")

class ReturnBookInputSerializer(serializers.Serializer):
    borrow_record_id = serializers.IntegerField(help_text="The ID of the borrow record to return.")