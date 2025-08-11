from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, MemberViewSet, BookViewSet, BorrowRecordViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'members', MemberViewSet)
router.register(r'books', BookViewSet)
router.register(r'borrow-records', BorrowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]