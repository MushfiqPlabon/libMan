from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Author, Member, Book, BorrowRecord
from .serializers import AuthorSerializer, MemberSerializer, BookSerializer, BorrowRecordSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    @action(detail=False, methods=['post'], url_path='borrow')
    def borrow_book(self, request):
        book_id = request.data.get('book_id')
        member_id = request.data.get('member_id')

        try:
            book = Book.objects.get(id=book_id)
            member = Member.objects.get(id=member_id)
        except (Book.DoesNotExist, Member.DoesNotExist):
            return Response({'error': 'Book or Member not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not book.availability_status:
            return Response({'error': 'Book is not available for borrowing.'}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record = BorrowRecord.objects.create(book=book, member=member)
        book.availability_status = False
        book.save()
        serializer = self.get_serializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='return')
    def return_book(self, request):
        borrow_record_id = request.data.get('borrow_record_id')

        try:
            borrow_record = BorrowRecord.objects.get(id=borrow_record_id, return_date__isnull=True)
        except BorrowRecord.DoesNotExist:
            return Response({'error': 'Active borrow record not found.'}, status=status.HTTP_404_NOT_FOUND)

        borrow_record.return_date = timezone.now().date()
        borrow_record.save()

        book = borrow_record.book
        book.availability_status = True
        book.save()
        serializer = self.get_serializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_200_OK)