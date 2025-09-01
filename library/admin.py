from django.contrib import admin
from .models import Book, Transaction

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id","title","author","isbn","copies_available","published_date")
    search_fields = ("title","author","isbn")
    list_filter = ("published_date",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id","user","book","status","checkout_date","return_date")
    list_filter = ("status",)
    search_fields = ("user__username","book__title","book__isbn")
