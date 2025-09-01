from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction as db_tx
from django.utils import timezone

from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author", "isbn"]

    def get_queryset(self):
        qs = super().get_queryset()
        available = self.request.query_params.get("available")
        if available is not None:
            if available.lower() in ["1","true","yes"]:
                qs = qs.filter(copies_available__gt=0)
            else:
                qs = qs.filter(copies_available__lte=0)
        return qs

    @action(detail=True, methods=["post"])
    def checkout(self, request, pk=None):
        book = self.get_object()
        with db_tx.atomic():
            book.refresh_from_db()
            if book.copies_available < 1:
                return Response({"detail": "No copies available."}, status=status.HTTP_400_BAD_REQUEST)
            exists = Transaction.objects.filter(user=request.user, book=book, status="OUT").exists()
            if exists:
                return Response({"detail": "You already have this book checked out."}, status=status.HTTP_400_BAD_REQUEST)
            trans = Transaction.objects.create(user=request.user, book=book, status="OUT")
            book.copies_available -= 1
            book.save()
        return Response(TransactionSerializer(trans).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        book = self.get_object()
        with db_tx.atomic():
            try:
                trans = Transaction.objects.select_for_update().get(user=request.user, book=book, status="OUT")
            except Transaction.DoesNotExist:
                return Response({"detail": "No active checkout to return."}, status=status.HTTP_400_BAD_REQUEST)
            trans.status = "RETURNED"
            trans.return_date = timezone.now()
            trans.save()
            book.copies_available += 1
            book.save()
        return Response(TransactionSerializer(trans).data)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)
