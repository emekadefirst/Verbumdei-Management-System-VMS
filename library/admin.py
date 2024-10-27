from django.contrib import admin
from .models import BookCategory, Shelf, Book, Loan


# Register BookCategory model
@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


# Register Shelf model
@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ["code", "location", "section", "description"]
    search_fields = ["code", "location", "section"]
    list_filter = ["section", "location"]
    readonly_fields = ["code"]


# Register Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "isbn",
        "copies",
        "category",
        "shelf",
        "created_at",
    ]
    search_fields = ["title", "author", "isbn"]
    list_filter = ["category", "shelf"]
    readonly_fields = ["created_at"]


# Register Loan model
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = [
        "book",
        "student",
        "action",
        "borrowed_at",
        "return_date",
        "actual_return_date",
    ]
    search_fields = ["book__title", "student__first_name", "student__last_name"]
    list_filter = ["action", "borrowed_at", "return_date"]
    date_hierarchy = "borrowed_at"
