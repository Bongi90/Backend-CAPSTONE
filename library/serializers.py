from rest_framework import serializers
from .models import Book, Transaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source="book.title")
    user_name = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Transaction
        fields = ["id","user","user_name","book","book_title","checkout_date","return_date","status"]
        read_only_fields = ["checkout_date","return_date","status"]
