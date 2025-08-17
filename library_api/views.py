from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db import transaction
from .models import Author, Member, Book, BorrowRecord
from .serializers import AuthorSerializer, MemberSerializer, BookSerializer, BorrowRecordSerializer, BorrowBookInputSerializer, ReturnBookInputSerializer
from .pagination import CustomPageNumberPagination

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPageNumberPagination

    @method_decorator(cache_page(60*5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows members to be viewed or edited.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPageNumberPagination

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    pagination_class = CustomPageNumberPagination

    @method_decorator(cache_page(60*5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class BorrowRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows borrow records to be viewed or edited.
    """
    queryset = BorrowRecord.objects.select_related('book', 'member').all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    @action(detail=False, methods=['post'], url_path='borrow')
    def borrow_book(self, request):
        """
        Borrows a book for a member.
        Expects 'book_id' and 'member_id' in the request body.
        Returns the created borrow record.
        """
        serializer = BorrowBookInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']
        member_id = serializer.validated_data['member_id']

        with transaction.atomic():
            try:
                book = Book.objects.select_for_update().get(id=book_id)
                member = Member.objects.select_for_update().get(id=member_id)
            except (Book.DoesNotExist, Member.DoesNotExist):
                return Response({'error': 'Book or Member not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Permission check: Only admin can borrow for other members
            # Regular users can only borrow for themselves
            if not request.user.is_staff:
                # Assuming Member model has a one-to-one relationship with User
                # If not, this logic needs adjustment based on how members are linked to users
                try:
                    user_member = Member.objects.get(user=request.user)
                    if user_member.id != member.id:
                        return Response({'error': 'You can only borrow for yourself.'}, status=status.HTTP_403_FORBIDDEN)
                except Member.DoesNotExist:
                    return Response({'error': 'User is not associated with a member account.'}, status=status.HTTP_400_BAD_REQUEST)

            if not book.availability_status:
                return Response({'error': 'Book is not available for borrowing.'}, status=status.HTTP_400_BAD_REQUEST)

            borrow_record = BorrowRecord.objects.create(book=book, member=member)
            book.availability_status = False
            book.save()
            response_serializer = self.get_serializer(borrow_record)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='return')
    def return_book(self, request):
        """
        Returns a borrowed book.
        Expects 'borrow_record_id' in the request body.
        Updates the borrow record and book availability.
        """
        serializer = ReturnBookInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrow_record_id = serializer.validated_data['borrow_record_id']

        with transaction.atomic():
            try:
                borrow_record = BorrowRecord.objects.select_for_update().get(id=borrow_record_id, return_date__isnull=True)
            except BorrowRecord.DoesNotExist:
                return Response({'error': 'Active borrow record not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Permission check: Only admin can return other users' books
            # Regular users can only return their own borrowed books
            if not request.user.is_staff:
                try:
                    user_member = Member.objects.get(user=request.user)
                    if borrow_record.member and borrow_record.member.id != user_member.id:
                        return Response({'error': 'You can only return your own borrowed books.'}, status=status.HTTP_403_FORBIDDEN)
                except Member.DoesNotExist:
                    return Response({'error': 'User is not associated with a member account.'}, status=status.HTTP_400_BAD_REQUEST)

            book = borrow_record.book
            if book and book.availability_status:
                return Response({'error': 'Book is already available.'}, status=status.HTTP_400_BAD_REQUEST)

            borrow_record.return_date = timezone.now().date()
            borrow_record.save()

            if book:
                book.availability_status = True
                book.save()
            response_serializer = self.get_serializer(borrow_record)
            return Response(response_serializer.data, status=status.HTTP_200_OK)